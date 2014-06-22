from django.conf.urls import patterns, url
from accounts.views import login_account

urlpatterns = patterns('',
                      url(r'^login_account/', login_account),
)
