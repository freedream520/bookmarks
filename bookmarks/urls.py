from django.conf.urls import *
from bookmark_base.views import *

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^photos/', include('photos.urls', namespace='photos')),
    (r'^login_account/', include('accounts.urls', namespace='accounts')),
    (r'^$', home),
    (r'^registe/', adduser),
    (r'^login/', 'django.contrib.auth.views.login'),
    (r'^logout/', logoutpage),
    (r'^registe_success/', registe_success),
    (r'^save/$', addmarks),
    (r'^tag/([^\s]+)/', tagpage),
    (r'^tag/$', tagcloundpage),
    (r'^search/$', search),
    (r'^user/(\w+)/$', userpage),
    (r'^friends/(\w+)/$', friendspage),
    (r'^friend/add/$', addfriend),
    (r'^vote/$', addvote),
    (r'^store/$', storeurl),
    (r'^delete/$', deleteurl),
    (r'^comments/$', include('django.contrib.comments.urls')),
    (r'^bookmark/(\d+)/$', bookmarkpage),
)
