import os
import sys

sys.path.append('/home/xinchao')
sys.path.append('/home/xinchao/bookmarks')

os.environ['DJANGO_SETTINGS_MODULE']='bookmarks.settings'

import django.core.handlers.wsgi

application=django.core.handlers.wsgi.WSGIHandler()
