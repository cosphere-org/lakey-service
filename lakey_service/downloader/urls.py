
from django.conf.urls import url

from . import commands


urlpatterns = [

    url(
        r'^render_ui_data/$',
        commands.DownloadRequestRenderCommands.as_view(),
        name='requests.render_ui_data'),

    url(
        r'^estimate/$',
        commands.DownloadRequestEstimateCommands.as_view(),
        name='requests.estimate'),

    url(
        r'^$',
        commands.DownloadRequestCollectionCommands.as_view(),
        name='requests.collection'),

    url(
        r'^(?P<request_id>\d+)$',
        commands.DownloadRequestElementCommands.as_view(),
        name='requests.element'),

]
