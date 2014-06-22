from django.conf.urls import patterns, include, url
from accounts.views import *

urlpatterns = patterns('',
    (r'^login_account/', login_account),
    url(r'^register/', add_user, name='register'),
    (r'^register_success/', register_success),
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/', logout_page, name='logout'),
    url(r'^user/(\w+)/$', user_page, name='user_page'),
)
