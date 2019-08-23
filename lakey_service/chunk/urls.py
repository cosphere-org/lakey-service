
from django.conf.urls import url

from . import commands


urlpatterns = [

    url(
        r'not_explored/',
        commands.ChunksNotExploredCommands.as_view(),
        name='chunks.not_explored'
    )
]
