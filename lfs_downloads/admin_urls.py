from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required

from .views import (
    ProductsListView, DigitalAssetsListView, UploadView, handle_upload,
    RelatedEditView, manage_digital_products, update_digiproducts
)

urlpatterns = patterns('',
    url(r'^lfsd_products_list$', ProductsListView.as_view(), name='lfsd_products_list'),
    url(r'^lfsd_files_list$', DigitalAssetsListView.as_view(), name='lfsd_files_list'),
    url(r'^lfsd_upload$', UploadView.as_view(), name='lfsd_upload'),
    url(r'^lfsd_handle_upload/(?P<product_id>\d*)$', handle_upload, name='lfsd_handle_upload'),
    url(r'^lfsd_update_digiproducts/(?P<product_id>\d*)$', update_digiproducts, name='lfsd_update_digiproducts'),
    url(r'^lfsd_manage_digital_products/(?P<product_id>\d*)$', manage_digital_products, name='lfsd_manage_digital_products'),
    url(r'^lfsd_related_products/(?P<product_id>\d*)$', RelatedEditView.as_view(), name='lfsd_related_products'),
)
