
from django.conf.urls import url

from . import views


urlpatterns = [

    url(
        r'^requests/render_ui_data/$',
        views.DownloadRequestRenderView.as_view(),
        name='requests.render_ui_data'),

    url(
        r'^requests/estimate/$',
        views.DownloadRequestEstimateView.as_view(),
        name='requests.estimate'),

    url(
        r'^requests/$',
        views.DownloadRequestCollectionView.as_view(),
        name='requests.collection'),

    url(
        r'^requests/(?P<request_id>\d+)$',
        views.DownloadRequestElementView.as_view(),
        name='requests.element'),

]
