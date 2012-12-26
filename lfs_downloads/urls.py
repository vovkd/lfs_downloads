from django.conf.urls.defaults import *
from .views import UserDownloadsListView

urlpatterns = patterns('',
    url(r'^my-downloads', UserDownloadsListView.as_view(), name="lfs_my_downloads"),
)
