
from django.conf.urls import url

from . import commands


urlpatterns = [

    url(
        r'^items/$',
        commands.CatalogueItemCollectionCommands.as_view(),
        name='items.collection'),

    url(
        r'^items/(?P<item_id>\d+)$',
        commands.CatalogueItemElementCommands.as_view(),
        name='items.element'),

]
