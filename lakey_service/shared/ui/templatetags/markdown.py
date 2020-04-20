
from django import template
from django.utils.safestring import mark_safe

from markdown import markdown as markdown_renderer


register = template.Library()


@register.simple_tag
def markdown(content):

    return mark_safe(markdown_renderer(content))
