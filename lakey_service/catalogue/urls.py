
from django.conf.urls import url

from . import views


urlpatterns = [

    url(
        r'^items/$',
        views.CatalogueItemCollectionView.as_view(),
        name='items.collection'),

    url(
        r'^items/(?P<item_id>\d+)$',
        views.CatalogueItemElementView.as_view(),
        name='items.element'),

]
