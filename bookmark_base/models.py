from django.db import models
from django.contrib.auth.models import User

class Url(models.Model):
    url=models.URLField(unique=True)
    def __unicode__(self):
        return self.url

class Bookmark(models.Model):
    title=models.CharField(max_length=100)
    uname=models.ForeignKey(User)
    link=models.ForeignKey(Url)
    def __unicode__(self):
        return u'%s , %s' %(self.uname.username,self.link.url)

class Tag(models.Model):
    content=models.CharField(max_length=100,unique=True)
    book=models.ManyToManyField(Bookmark)
    def __unicode__(self):
        return content

class ShareItem(models.Model):
    bookmark=models.ForeignKey(Bookmark)
    datetimeField=models.DateTimeField(auto_now=True)
    votes=models.IntegerField(default=1)
    uvote=models.ManyToManyField(User)

class Freindship(models.Model):
    fromuser=models.ForeignKey(User,related_name='friend_set')
    touser=models.ForeignKey(User,related_name='to_friend_set')
    class Meta:
        unique_together=(('fromuser','touser'),)   
