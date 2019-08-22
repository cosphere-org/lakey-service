
from django.conf.urls import url, include


urlpatterns = [

    url(
        r'^accounts/',
        include(
            ('account.urls', 'account'),
            namespace='account')),

    url(
        r'^catalogue/items/',
        include(
            ('catalogue.urls', 'catalogue'),
            namespace='catalogue')),

    url(
        r'^catalogue/items/(?P<catalogue_item_id>\d+)/chunks/',
        include(
            ('chunk.urls', 'chunk'),
            namespace='chunk')),

    url(
        r'^downloader/requests/',
        include(
            ('downloader.urls', 'downloader'),
            namespace='downloader')),

    url(
        r'^',
        include(
            ('lily.entrypoint.urls', 'entrypoint'),
            namespace='entrypoint')),

]
