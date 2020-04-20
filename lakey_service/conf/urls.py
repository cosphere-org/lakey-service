
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    #
    # ADMIN
    #
    url(
        r'^admin/',
        admin.site.urls
    ),

    #
    # API
    #
    url(
        r'^accounts/',
        include(
            ('account.urls', 'account'),
            namespace='account')),

    url(
        r'^catalogue/',
        include(
            ('catalogue.urls', 'catalogue'),
            namespace='catalogue')),

    url(
        r'^downloader/',
        include(
            ('downloader.urls', 'downloader'),
            namespace='downloader')),

    url(
        r'^',
        include(
            ('lily.entrypoint.urls', 'entrypoint'),
            namespace='entrypoint')),

    #
    # UI
    #
    url(
        r'^ui/accounts/',
        include(
            ('account.ui.urls', 'account'),
            namespace='account_ui')),

    url(
        r'^ui/catalogue/',
        include(
            ('catalogue.ui.urls', 'catalogue'),
            namespace='catalogue_ui')),

    url(
        r'^ui/downloader/',
        include(
            ('downloader.ui.urls', 'downloader'),
            namespace='downloader_ui')),

]
