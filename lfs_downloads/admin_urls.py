from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required

from .views import ProductsListView, UploadView, handle_upload

urlpatterns = patterns('',
    url(r'^lfsd_products_list$', ProductsListView.as_view(), name='lfsd_products_list'),
    url(r'^lfsd_upload$', UploadView.as_view(), name='lfsd_upload'),
    url(r'^lfsd_handle_upload$', handle_upload, name='lfsd_handle_upload'),
)
