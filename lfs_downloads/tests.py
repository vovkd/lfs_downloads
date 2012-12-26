import os
import shutil
from django.test import TestCase
from django.conf import settings
from lfs.catalog.models import Product
from lfs.tax.models import Tax
from lfs_downloads.models import DigitalAsset


class ModelsTestCase(TestCase):

    def setUp(self):
        self.tax = Tax.objects.create(rate=17.0)
        self.p1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            price=10.0,
            tax=self.tax,
            active=True
        )
        self.tempdir = os.tempnam()
        self.pubdir = os.path.join(self.tempdir, 'public')
        self.privdir = os.path.join(self.tempdir, 'private')
        os.mkdir(self.tempdir)
        os.mkdir(self.pubdir)
        os.mkdir(self.privdir)
        self.old_pubdir = getattr(settings, 'LFS_DOWNLOADS_PUBLIC_FOLDER', None)
        self.old_privdir = getattr(settings, 'LFS_DOWNLOADS_PRIVATE_FOLDER', None)
        setattr(settings, 'LFS_DOWNLOADS_PUBLIC_FOLDER', self.pubdir)
        setattr(settings, 'LFS_DOWNLOADS_PRIVATE_FOLDER', self.privdir)

    def tearDown(self):
        setattr(settings, 'LFS_DOWNLOADS_PUBLIC_FOLDER', self.old_pubdir)
        setattr(settings, 'LFS_DOWNLOADS_PRIVATE_FOLDER', self.old_privdir)
        shutil.rmtree(self.tempdir)

    def testDigitalAsset(self):
        asset = DigitalAsset.objects.create(file = 'xx', product=self.p1)
        