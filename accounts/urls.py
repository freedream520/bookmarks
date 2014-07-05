from django.conf.urls import patterns, include, url
from accounts.views import *

urlpatterns = patterns('',
    url(r'^login/', login, name='login'),
    url(r'^add_user/', add_user, name='add_user'),
    url(r'^register/', register, name='register'),
    (r'^register_success/', register_success),
    url(r'^pc_login/', 'django.contrib.auth.views.login', name='pc_login'),
    url(r'^logout/', logout_page, name='logout'),
    url(r'^user/(\w+)/$', user_page, name='user_page'),
)
