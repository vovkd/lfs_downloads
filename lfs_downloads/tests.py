from unittest import TestCase
from django.test import TestCase
from django.contrib.sessions.backends.file import SessionStore

from lfs.catalog.models import Product
from lfs.tax.models import Tax
from lfs.tests.utils import RequestFactory
from lfs.catalog.settings import PRODUCT_WITH_VARIANTS, VARIANT


class LFSDownloadsTestCase(TestCase):
    """
    Test lfs_downloads

    LFS downloads react when user buys a product. It doesn't care what kind of
    product has been bought. If the product 
    """
    fixtures = ['lfs_shop.xml']

    def setUp(self):
        """
        """
        self.request = RequestFactory().get("/")
        self.request.session = SessionStore()

        # Create a product
        # LFS downloads does not depend upon properties 
        self.p1 = Product.objects.create(
            name=u"My Product",
            slug=u"my-product",
            sku=u"SKU MYPR",
            description=u"Description",
            short_description=u"Short description my product",
            meta_description=u"Meta description my product",
            meta_keywords=u"Meta keywords my product",
            price=1.0,
            active=True
        )

        # setup attachments test stuff
        self.setupAttachments()
