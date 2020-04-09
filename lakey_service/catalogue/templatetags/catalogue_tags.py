
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
    graphs_html = '<div id="wrap" style="overflow:scroll; height:600px;">'
    for column in spec:
        distribution = column['distribution']
        if distribution is not None:
            fig = px.bar(distribution,
                         x='value', y='count',
                         title=column['name'])
            graph_html = fig.to_html(full_html=False,
                                     default_height=500,
                                     default_width=700)
            graphs_html += graph_html
    graphs_html += '</div>'
    return mark_safe(graphs_html)

# TODO: review/test correctness in case of missing distributions
@register.simple_tag
def distribution_chart_2(spec):

    titles = [s['name'] for s in spec if s['distribution'] is not None]
    no_of_charts = len(titles)

    if no_of_charts == 0:
        return 'No distribution data'

    fig = make_subplots(rows=1, cols=no_of_charts,
                        subplot_titles=titles)
    col_nr = 1
    for s in spec:
        d = s['distribution']
        if d is not None:
            values = [i['value'] for i in d]
            counts = [i['count'] for i in d]

            fig.add_trace(
                go.Bar(x=values, y=counts),
                row=1, col=col_nr
            )
            col_nr += 1

    fig.update_layout(height=400,
                      width=no_of_charts*400,
                      showlegend=False)
    graph_html = '<div style ="overflow-x: auto;" >'
    graph_html += fig.to_html(full_html=False)
    graph_html += '</div>'

    return mark_safe(graph_html)
