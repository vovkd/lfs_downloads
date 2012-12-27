from django.db import models
from django.contrib.auth.models import User
from lfs.order.models import OrderItem
from lfs.catalog.models import Product

from .settings import LFS_DOWNLOADS_PRIVATE_FOLDER, LFS_DOWNLOADS_DOWNLOAD_LIMIT
from .storage import LFSDownloadsHiddenStorage


class DigitalAsset(models.Model):   
    file = models.FileField(upload_to='%Y/%m/%d', storage=LFSDownloadsHiddenStorage())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product)


class DownloadDelivery(models.Model):
    """
    When the user buys a DigitalAsset, a DownloadDelivery record will be
    created.
    """
    user = models.ForeignKey(User, blank=True, null=True)
    order = models.ForeignKey(OrderItem, blank=True, null=True, on_delete=models.SET_NULL)
    downloaded_at = models.DateField()
    download_count = models.IntegerField()

    @property
    def available(self):
        return self.download_count < LFS_DOWNLOADS_DOWNLOAD_LIMIT
