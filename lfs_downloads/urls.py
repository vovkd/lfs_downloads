from django.conf.urls.defaults import *
from .views import UserDownloadsListView, download_proxy_view

urlpatterns = patterns('',
    url(r'^my-downloads$', UserDownloadsListView.as_view(), name="lfsd_library"),
    url(r'^my-downloads/(?P<pk>\d+)$', download_proxy_view, name="lfsd_download_proxy"),
)
