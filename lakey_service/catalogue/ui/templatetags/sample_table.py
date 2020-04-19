
import pandas as pd

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def sample_table(sample):
    df = pd.DataFrame(sample)
    df_html = df.to_html(index=False).replace('\n', '')
    return mark_safe(df_html)
