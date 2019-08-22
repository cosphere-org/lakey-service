
from django.conf.urls import url

from . import commands


urlpatterns = [

    url(
        r'^$',
        commands.CatalogueItemCollectionCommands.as_view(),
        name='items.collection'),

    url(
        r'^(?P<item_id>\d+)$',
        commands.CatalogueItemElementCommands.as_view(),
        name='items.element'),

    url(
        r'^(?P<item_id>\d+)/samples_and_distributions/$',
        commands.CatalogueItemSampleAndDistributionsCommands.as_view(),
        name='items.element.samples_and_distributions'),

]
