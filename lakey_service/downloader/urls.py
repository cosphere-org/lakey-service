
from django.conf.urls import url

from . import commands


urlpatterns = [

    url(
        r'^requests/render_ui_data/$',
        commands.DownloadRequestRenderCommands.as_view(),
        name='requests.render_ui_data'),

    url(
        r'^requests/estimate/$',
        commands.DownloadRequestEstimateCommands.as_view(),
        name='requests.estimate'),

    url(
        r'^requests/$',
        commands.DownloadRequestCollectionCommands.as_view(),
        name='requests.collection'),

    url(
        r'^requests/(?P<request_id>\d+)$',
        commands.DownloadRequestElementCommands.as_view(),
        name='requests.element'),

]
