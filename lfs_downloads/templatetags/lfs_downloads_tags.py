from django.template import Library
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from lfs_downloads.views import manage_digital_products

register = Library()

@register.simple_tag(takes_context=True)
def lfs_downloads_management(context, product):
    request = context.get('request', None)  # we rely on request context processor

    result = manage_digital_products(request, product.id, as_string=True)
    return mark_safe(result)

@register.filter('has_donation_mode')
def has_donation_mode (product):
    return product.digitalasset_set.filter(donation_mode=True).count()
