from django.conf.urls import *
from bookmark_base.views import *

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^photos/', include('photos.urls', namespace='photos')),
    (r'^account/', include('accounts.urls', namespace='accounts')),

    (r'^$', home),



    (r'^save/$', addmarks),
    (r'^tag/([^\s]+)/', tagpage),
    (r'^tag/$', tagcloundpage),
    (r'^search/$', search),

    (r'^friends/(\w+)/$', friendspage),
    (r'^friend/add/$', addfriend),
    (r'^vote/$', addvote),
    (r'^store/$', storeurl),
    (r'^delete/$', deleteurl),
    (r'^comments/$', include('django.contrib.comments.urls')),
    (r'^bookmark/(\d+)/$', bookmarkpage),
)
