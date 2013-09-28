import os

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from lfs.order.models import OrderItem
from lfs.catalog.models import Product
from lfs.core.signals import order_paid

from .settings import LFS_DOWNLOADS_PRIVATE_FOLDER, LFS_DOWNLOADS_DOWNLOAD_LIMIT
from .storage import LFSDownloadsHiddenStorage


class DigitalAsset(models.Model):
    """
    Links a product with a file that will be delivered
    """
    file = models.FileField(upload_to='%Y/%m/%d', storage=LFSDownloadsHiddenStorage())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, null=True)
    donation_mode = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('lfsd_download_proxy', args=[str(self.id)])

    def __unicode__(self):
        if self.product:
            return "DigitalAsset for %s" % (self.product.name)
        else:
            return super(self, DigitalAsset).__unicode__()

    def get_filename(self):
        return os.path.basename(self.file.name)

    def get_filesize(self):
        return self.file.size

class DownloadDelivery(models.Model):
    """
    When the user buys a DigitalAsset, a DownloadDelivery record will be
    created.
    """
    user = models.ForeignKey(User, blank=True, null=True)
    order = models.ForeignKey(OrderItem, blank=True, null=True, on_delete=models.SET_NULL)
    downloaded_at = models.DateField(null=True)
    download_count = models.IntegerField(default=0)
    asset = models.ForeignKey(DigitalAsset)
    product = models.ForeignKey(Product, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('lfsd_download_proxy', args=[str(self.id)])

    @property
    def downloads_left (self):
        return LFS_DOWNLOADS_DOWNLOAD_LIMIT - self.download_count

    @property
    def available(self):
        return self.download_count < LFS_DOWNLOADS_DOWNLOAD_LIMIT

@receiver(order_paid)
def find_digital_downloads_in_order(sender, **kwargs):
    order =  sender['order']
    oitems = OrderItem.objects.filter(order=order)
    products = [oitm.product for oitm in oitems]
    for p in products:
        d = DownloadDelivery(
            user = order.user,
            order = oitm,
            asset = DigitalAsset.objects.get(product__id=p.id)
        )
        d.save()
