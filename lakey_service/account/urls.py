
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import commands, views


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

    url(
        r'^get_token/$',
        commands.GetTokenUICommands.as_view(),
        name='auth.get_token.ui'),
    
    url(
        r'^generate_token/$',
        commands.GenerateTokenCommands.as_view(),
        name='auth.get_token.ui'),

    url(
        r'^login/$',
        auth_views.LoginView.as_view(),
        name='auth.login'
    ),

        url(
        r'^$',
        login_required(views.DashboardView.as_view()),
        name='auth.dashboard'
    ),

    url(
        r'(?P<item_id>[\w\-]+)/$',
        views.catalogue_item_view,
        name='auth.catalogue_item'),
]
