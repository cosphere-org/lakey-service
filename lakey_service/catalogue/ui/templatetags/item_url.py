
from django.urls import reverse

from django import template


register = template.Library()


@register.simple_tag
def item_url(item):

    return reverse(
        'catalogue_ui:ui.catalogue.element',
        args=[item.id])
