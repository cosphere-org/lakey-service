
from django.conf.urls import url

from . import views


urlpatterns = [

    url(
        r'^auth_requests/$',
        views.AuthRequestView.as_view(),
        name='auth.requests'),

    url(
        r'^auth_requests/(?P<request_uuid>[\w\-]+)/authenticate/ui/$',
        views.AuthRequestAuthenticateUIView.as_view(),
        name='auth.requests.authenticate.ui'),

    url(
        r'^auth_requests/attach_account/$',
        views.AuthRequestAttachAccountView.as_view(),
        name='auth.requests.attach_account'),

    url(
        r'^auth_tokens/$',
        views.AuthTokenView.as_view(),
        name='auth.auth_token'),

]
