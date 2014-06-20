from django.conf.urls import *
from bookmark_base.views import *

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
       # Example:
       # (r'^bookmarks/', include('bookmarks.foo.urls')),

       # Uncomment the admin/doc line below to enable admin documentation:
       # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

       (r'^admin/', include(admin.site.urls)),
       (r'^$', home),
       (r'^registe/', adduser),
       (r'^login/', 'django.contrib.auth.views.login'),
       (r'^logout/', logoutpage),
       (r'^registe_success/', registe_successr),
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
