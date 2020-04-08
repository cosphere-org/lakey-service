
import pandas as pd
import plotly.express as px

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def sample_table(sample):
    print(f"sample: {sample}")
    df = pd.DataFrame(sample)
    df_html = df.to_html(index=False).replace('\n', '')
    return mark_safe(df_html)

# TODO: iterate one level above(?)
@register.simple_tag
def distribution_chart(spec):
    print(f"Spec: {spec}")
    graphs_html = ""
    for column in spec:
        distribution = column['distribution']
        if distribution is not None:
            fig = px.bar(distribution,
                         x='value', y='count',
                         title=column['name'])
            graph_html = fig.to_html(full_html=False,
                                     default_height=500,
                                     default_width=700)
            graphs_html += graph_html+'</br>'
    return mark_safe(graphs_html)
