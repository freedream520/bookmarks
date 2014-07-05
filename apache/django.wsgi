import os
import sys

sys.path.append('c:/wamp/www/bookmarks')

os.environ['DJANGO_SETTINGS_MODULE']='bookmarks.settings'

import django.core.handlers.wsgi

application=django.core.handlers.wsgi.WSGIHandler()
