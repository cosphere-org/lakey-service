
from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^$',
        views.CatalogueItemsCollectionView.as_view(),
        name='ui.catalogue.collection'
    ),

    url(
        r'^(?P<item_id>\d+)$',
        views.CatalogueItemElementView.as_view(),
        name='ui.catalogue.element'
    ),

]
