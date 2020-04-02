
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),

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

]
