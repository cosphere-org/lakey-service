
from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^create_for_catalogue/(?P<item_id>\d+)$',
        views.DownloadRequestCreateView.as_view(),
        name='ui.request.create_for_catalogue'
    ),

    url(
        r'^requests/$',
        views.DownloadRequestCollectionView.as_view(),
        name='ui.request.collection'
    ),

]
