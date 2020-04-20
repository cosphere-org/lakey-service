
from django.urls import reverse

from django import template


register = template.Library()


@register.simple_tag
def download_item_url(item):

    return reverse(
        'downloader_ui:ui.request.create_for_catalogue',
        args=[item.id])
