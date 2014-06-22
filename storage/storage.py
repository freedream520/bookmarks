#coding=utf-8
"""
真正有用的sae存储
"""
from os import environ
debug = not environ.get("APP_NAME", '')
#if not debug:#其实改storage就可以了，网上的代码没有我的好，common的file废了
#    from stock.common.file import ZGImageField,ZGFileField
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.conf import settings
import time,os,uuid,random,unicodedata,StringIO
from django.core.files.base import ContentFile
if not debug:
    import sae
    import tempfile
    import sae.storage
    from PIL import Image
else:
    import Image

class SaeAndNotSaeStorage(FileSystemStorage):
    """
    修改存储文件的路径和基本url
    """
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(SaeAndNotSaeStorage, self).__init__(location, base_url)
    
    def is_chinese(self,uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'u4e00' and uchar<=u'u9fa5':
            return True
        else:
            return False
    
    def get_valid_name(self, name):
        """
        这个方法用于验证文件名,很重要
        """
        #name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        #处理中文文件名sae不支持
        if not debug:
            try:
                if 1:
                    #去掉中文
                    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
                else:
                    for k in name:
                        if self.is_chinese(k):
                            name = "wszw%s"%random.randint(0,100)
            except Exception,e:
                name = "%s.jpg"%type(name)
        #end
        return super(SaeAndNotSaeStorage, self).get_valid_name(name)
    
    @property
    def maxsize(self):
        return 10*1024*1024#文件2M--sae限制只能传2M,单个文件，据说是10M,其实只有2M
    
    @property
    def filetypes(self):
        return []
    
    def makename(self,name):
        #取一个不重复的名字，sae会把重名覆盖
        oname = os.path.basename(name)
        path = os.path.dirname(name)
        #首先判断是否需要重命名---也就是说不想改名字的就加这个前缀
        if oname.find("_mine_")==0:
            oname = oname.replace("_mine_","")
            name = os.path.join(path, oname)
            return name
        #end---首先判断是否需要重命名
        try:
            fname, hk = oname.split(".")
        except Exception,e:
            fname, hk = oname, ''
        if hk:
            rname  = "%s_%s.%s"%(random.randint(0,10000), fname,hk)
        else:
            rname  = "%s_%s"%(random.randint(0,10000), fname)
        name = os.path.join(path, rname)
        #end
        return name
    
    def _save(self, name, content):
        """
        可以判断上传哪些文件
        """
        hz = name.split(".")[-1]
        #类型判断
        if self.filetypes!='*':
            if hz.lower() not in self.filetypes:
                raise SuspiciousOperation(u"不支持的文件类型,支持%s"%self.filetypes)
        #end
        name = self.makename(name)
        #大小判断
        if content.size > self.maxsize:
            raise SuspiciousOperation(u"文件大小超过限制")
        #end
        #保存
        if not debug:
            s = sae.storage.Client()
            if hasattr(content, '_get_file'):#admin入口
                ob = sae.storage.Object(content._get_file().read())
            else:#view入口（ContentFile）
                ob = sae.storage.Object(content.read())
            url =s.put('media', name, ob)
            return name
        else:
            return super(SaeAndNotSaeStorage, self)._save(name, content)
        #end--保存
     
    def delete(self,name):
        """
        """
        if not debug:
            s = sae.storage.Client()
            try:
                s.delete('media', name)
            except Exception,e:
                pass
        else:
            super(SaeAndNotSaeStorage, self).delete(name)

class ImageStorage(SaeAndNotSaeStorage):
    @property
    def maxsize(self):
        return 2*1024*1024#文件2M
    
    @property
    def filetypes(self):
        return ['jpg','jpeg','png','gif']

class FileStorage(SaeAndNotSaeStorage):
    @property
    def maxsize(self):
        return 10*1024*1024#文件5M
    
    @property
    def filetypes(self):
        return "*"
    
    #def makename(self, name):
    #    return name


class ThumbStorage(ImageStorage):
    """
    缩略图
    """ 
    def _save(self, name, content):
        #处理
        image = Image.open(content)
        image = image.convert('RGB')
        image.thumbnail((50, 50), Image.ANTIALIAS)
        
        output = StringIO.StringIO()
        image.save(output,'JPEG')
        co = ContentFile(output.getvalue())
        output.close()
        #end
        return super(ThumbStorage, self)._save(name, co)
        
