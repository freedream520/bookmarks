from django.conf.urls import *
from photos.views import *

urlpatterns = patterns('',
    url('upload/', add_photo)
)