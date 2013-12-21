#Pythonic
import os.path
from datetime import datetime

#Django madness
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView, UpdateView

#lfs's spaghetti :D
from lfs.caching.utils import lfs_get_object_or_404
from lfs.catalog.models import Product
from lfs.core.signals import product_changed
from lfs.core.utils import LazyEncoder

#My own mess
from .models import DigitalAsset, DownloadDelivery
from .sendfile import xsendfileserve
from .forms import DonationAdminForm


class ManageMixin(object):
    @method_decorator(permission_required("core.manage_shop", login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(ManageMixin, self).dispatch(request, *args, **kwargs)

class SimpleSecurityMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SimpleSecurityMixin, self).dispatch(request, *args, **kwargs)


#User pages and views

class UserDownloadsListView(SimpleSecurityMixin, ListView):
    model = DownloadDelivery
    template_name = 'lfs_downloads/library.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

@login_required
def download_proxy_view(request, pk):
    delivery = lfs_get_object_or_404(DownloadDelivery, id=pk)
    if delivery.available:
        delivery.download_count += 1
        delivery.downloaded_at = datetime.now()
        delivery.save()
        #Now, go look for the file and serve it.
        opath = delivery.asset.file.path
        dpath = os.path.dirname(opath)
        fname = os.path.basename(opath)
        return xsendfileserve(request=request, path=fname, document_root=dpath)
    else:
        return HttpResponseForbidden()

#Admin pages and views
class ProductsListView(ManageMixin, ListView):
    model = Product
    template_name = 'lfs_downloads/manage_products_list.html'

    def file_list(self):
        return [
            {'name': 'LMTEPU.pdf', 'size': '645Kb', 'uploaded': '10/23/12 05:59 PM'},
            {'name': 'LPDLM.pdf', 'size': '645Kb', 'uploaded': '10/23/12 05:59 PM'},
            {'name': 'Seminario I - Argentina.avi', 'size': '45645Kb', 'uploaded': '10/23/12 05:59 PM'},
            {'name': 'Seminario I - Argentina.avi', 'size': '545645Kb', 'uploaded': '10/23/12 05:59 PM'},
        ]

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['file_list'] = self.file_list()
        return context


class DigitalAssetsListView(ManageMixin, ListView):
    model = DigitalAsset
    template_name = 'lfs_downloads/manage_files_list.html'


class UploadView(ManageMixin, TemplateView):
    template_name = 'lfs_downloads/manage_upload.html'


class RelatedEditView(UpdateView):
    model = DigitalAsset
    template_name = 'lfs_downloads/manage_related.html'


@permission_required("core.manage_shop", login_url="/login/")
def manage_download_digital_product(request, asset_id):
    asset = get_object_or_404(DigitalAsset, pk=asset_id)
    opath = asset.file.path
    dpath = os.path.dirname(opath)
    fname = os.path.basename(opath)
    return xsendfileserve(request=request, path=fname, document_root=dpath)
    

@permission_required("core.manage_shop", login_url="/login/")
def manage_digital_products(request, product_id, as_string=False,
                   template_name="lfs_downloads/manage_digital_products.html"):
    product = lfs_get_object_or_404(Product, pk=product_id)
    digiproducts = DigitalAsset.objects.filter(product=product).all()
    donation_mode = DigitalAsset.objects.filter(product=product, donation_mode=True).all()
    minimum_price = '1.0'
    suggested_price = '10.0'
    if len(digiproducts):
        minimum_price = digiproducts[0].minimum_price
        suggested_price = digiproducts[0].suggested_price

    result = render_to_string(template_name,RequestContext(request, {
        "product": product,
        "digiproducts": digiproducts,
        "has_digiproducts": len(digiproducts),
        "donation_mode": len(donation_mode),
        'minimum_price': minimum_price,
        'suggested_price': suggested_price,
    }))

    if as_string:
        return result
    else:
        result = simplejson.dumps({
            "html_data": result,
            "message": _(u"New attachment."),
        }, cls=LazyEncoder)

        return HttpResponse(result)

@permission_required("core.manage_shop", login_url="/login/")
def handle_upload(request, product_id):
    """
        Handles upload of new DigitalAsset
    """
    product = lfs_get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        for file_content in request.FILES.getlist("files"):
            digiproduct = DigitalAsset(file=file_content, product=product)
            digiproduct.file.save(file_content.name, file_content, save=True)

    product_changed.send(product, request=request)
    return manage_digital_products(request, product_id)

@permission_required("core.manage_shop", login_url="/login/")
def update_digiproducts(request, product_id):
    """
        Just to delete digital products with given ids (passed by request body).
        Maybe later have some description.
    """
    product = lfs_get_object_or_404(Product, pk=product_id)
    action = request.POST.get("action")
    message = _(u"Digital Product has been updated.")

    if action == "delete":
        message = _(u"Digital Product has been deleted.")
        for key in request.POST.keys():
            if key.startswith("delete-"):
                try:
                    id = key.split("-")[1]
                    digiproduct = DigitalAsset.objects.get(pk=id).delete()
                except (IndexError, ObjectDoesNotExist):
                    pass
    if action == 'update_donation_mode':
        product = lfs_get_object_or_404(Product, pk=product_id)
        message = _(u"Donation mode has been updated.")
        DigitalAsset.objects.filter(product=product).update(
            donation_mode=request.POST.get('donation_mode', False),
            minimum_price=request.POST.get('minimum_price', '1.0'),
            suggested_price=request.POST.get('suggested_price', '1.0'),
        )

    product_changed.send(product, request=request)

    html = [["#lfs_downloads", manage_digital_products(request, product_id, as_string=True)]]
    result = simplejson.dumps({
        "html": html,
        "message": message,
    }, cls=LazyEncoder)

    return HttpResponse(result)
