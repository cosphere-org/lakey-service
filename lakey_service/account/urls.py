
from django.conf.urls import url

from . import commands


urlpatterns = [

    #
    # AUTH REQUESTS FLOW
    #
    url(
        r'^auth_requests/$',
        commands.AuthRequestCommands.as_view(),
        name='auth.requests'),

    url(
        r'^auth_requests/attach_account/$',
        commands.AuthRequestAttachAccountCommands.as_view(),
        name='auth.requests.attach_account'),

    url(
        r'^auth_requests/auth_tokens/$',
        commands.AuthRequestAuthTokenCommands.as_view(),
        name='auth.requests.auth_token'),

    #
    # UI FLOW
    #
    url(
        r'^auth_tokens/$',
        commands.AuthTokenCommands.as_view(),
        name='auth.auth_token'),

]
