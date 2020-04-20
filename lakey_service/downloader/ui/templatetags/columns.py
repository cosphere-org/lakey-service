
from django import template


register = template.Library()


@register.simple_tag
def columns(spec):
    return ', '.join(spec['columns'])
