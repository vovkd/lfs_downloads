from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.backends.file import SessionStore
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase
from django.test.client import Client
from django.core import mail

from lfs.tests.utils import RequestFactory, DummyRequest
from lfs.core.models import Country
from lfs.customer.models import Address
from lfs.customer.models import Customer
from lfs.tests.utils import create_request
from lfs.catalog.models import Product
from lfs.core.utils import get_default_shop
from lfs_downloads.models import DigitalAsset



class LFSDownloadsTestCase(TestCase):
    """
    Test lfs_downloads

    LFS downloads react when user buys a product. It doesn't care what kind of
    product has been bought. If the product 
    """
    fixtures = ['lfs_shop.xml']

    def setUp(self):
        # User
        self.username = 'David'
        self.password = 'Bohm'
        self.email = 'd.bohm@holokinesis.org'
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.product = Product.objects.create(
            name="Product 1",
            slug="product-1",
            sku="sku-1",
            price=1.1,
            active=True,
        )
        self.product.save()


        # Create a digital asset
        self.asset = DigitalAsset(
            product=self.product
        )
        self.asset.save()


    def test_digital_delivery(self):
        self.client.login(username=self.user, password=self.password)
        #Now simulate a user paying a product. No need for Paypal

