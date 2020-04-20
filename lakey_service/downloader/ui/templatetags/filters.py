
from django import template


register = template.Library()


@register.simple_tag
def filters(spec):
    def filter(f):
        name = f['name']
        operator = f['operator']
        value = f['value']

        return f'{name} {operator} {value}'

    return ', '.join([filter(f) for f in spec['filters']])
