import os.path
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.forms import forms
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView, UpdateView

from lfs.catalog.models import Product
from lfs.core.utils import LazyEncoder
from lfs.caching.utils import lfs_get_object_or_404

from .models import DigitalAsset, DownloadDelivery
from .sendfile import xsendfileserve

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


@permission_required("core.manage_shop", login_url="/login/")
def handle_upload(request):
    """
        Handles upload of new DigitalAsset
    """
    if request.method == "POST":
        for file_content in request.FILES.getlist("files"):
            digiasset = DigitalAsset(file=file_content)
            digiasset.file.save(file_content.name, file_content, save=True)
        return HttpResponse(simplejson.dumps(
            {'message': _(u'%s files uploaded') % len(request.FILES)}, 
            cls=LazyEncoder)
        )
    return HttpResponse(simplejson.dumps(   
        {'message': _(u'F   iles uploaded')}, 
        cls=LazyEncoder)
    )

class RelatedEditView(UpdateView):
    model = DigitalAsset
    template_name = 'lfs_downloads/manage_related.html'
