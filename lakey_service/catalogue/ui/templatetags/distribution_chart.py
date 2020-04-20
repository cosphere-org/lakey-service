
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def distribution_chart(spec):

    titles = [s['name'] for s in spec if s['distribution'] is not None]
    no_of_charts = len(titles)

    if no_of_charts == 0:
        return mark_safe('No distribution data')

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

    fig.update_layout(
        height=400,
        width=no_of_charts * 400,
        showlegend=False)

    return mark_safe(
        '<div style ="overflow-x: auto;" >' +
        fig.to_html(full_html=False) +
        '</div>')
