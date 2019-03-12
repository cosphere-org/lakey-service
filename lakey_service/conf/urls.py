
from django.conf.urls import url, include


urlpatterns = [

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
        r'^',
        include(
            ('lily.entrypoint.urls', 'entrypoint'),
            namespace='entrypoint')),

]
