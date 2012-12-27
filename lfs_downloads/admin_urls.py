from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required

from .views import ProductsListView, DigitalAssetsListView, UploadView, handle_upload, RelatedEditView

urlpatterns = patterns('',
    url(r'^lfsd_products_list$', ProductsListView.as_view(), name='lfsd_products_list'),
    url(r'^lfsd_files_list$', DigitalAssetsListView.as_view(), name='lfsd_files_list'),
    url(r'^lfsd_upload$', UploadView.as_view(), name='lfsd_upload'),
    url(r'^lfsd_handle_upload$', handle_upload, name='lfsd_handle_upload'),
    url(r'^lfsd_related_products/(?P<pk>\d*)$', RelatedEditView.as_view(), name='lfsd_related_products'),
)
