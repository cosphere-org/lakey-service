
from django.conf.urls import url

from . import commands


urlpatterns = [

    url(
        r'^auth_requests/$',
        commands.AuthRequestCommands.as_view(),
        name='auth.requests'),

    url(
        r'^auth_requests/(?P<request_uuid>[\w\-]+)/authenticate/ui/$',
        commands.AuthRequestAuthenticateUICommands.as_view(),
        name='auth.requests.authenticate.ui'),

    url(
        r'^auth_requests/attach_account/$',
        commands.AuthRequestAttachAccountCommands.as_view(),
        name='auth.requests.attach_account'),

    url(
        r'^auth_tokens/$',
        commands.AuthTokenCommands.as_view(),
        name='auth.auth_token'),

]
