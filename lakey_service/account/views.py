
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from lily import (
    command,
    Input,
    Meta,
    name,
    Output,
    parsers,
    serializers,
)
from django.template.loader import render_to_string

from .domains import ACCOUNT_AUTHENTICATION
from .models import AuthRequest
from .serializers import AuthTokenSerializer, AuthRequestSerializer


class AuthRequestView(View):

    @command(
        name=name.Create('AUTH_REQUEST'),

        meta=Meta(
            title='Create Auth Request',
            domain=ACCOUNT_AUTHENTICATION),

        output=Output(serializer=AuthRequestSerializer),
    )
    def post(self, request):

        r = AuthRequest.objects.create()

        raise self.event.Created({
            # 'ui_uri': 'https://lakey.eu.ngrok.io/authentications/ui/',
            'authenticate_ui_uri': reverse(
                'account:auth.requests.authenticate.ui',
                kwargs={'request_uuid': r.uuid}),
            'request_uuid': r.uuid,
        })


class AuthRequestAuthenticateUIView(View):

    @command(
        name=name.Execute('RENDER', 'AUTH_REQUEST_AUTHENTICATE_UI'),

        meta=Meta(
            title='Render Auth Request Authentication UI',
            domain=ACCOUNT_AUTHENTICATION),
    )
    def get(self, request, request_uuid):

        return HttpResponse(render_to_string(
            'authenticate.html',
            {
                'auth_request_uuid': request_uuid,
                'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            }))


class AuthRequestAttachAccountView(View):

    class BodyParser(parsers.BodyParser):

        request_uuid = parsers.UUIDField()

        code = parsers.CharField()

        email = parsers.EmailField()

    @command(
        name=name.Execute('ATTACH', 'ACCOUNT_TO_AUTH_REQUEST'),

        meta=Meta(
            title='Attach Account to Auth Request',
            domain=ACCOUNT_AUTHENTICATION),

        input=Input(body_parser=BodyParser),

        output=Output(serializer=serializers.EmptySerializer),
    )
    def post(self, request):

        AuthRequest.objects.get(
            uuid=request.input.body['request_uuid']
        ).attach_account(
            email=request.input.body['email'],
            authorization_code=request.input.body['code'])

        raise self.event.Executed()


class AuthTokenView(View):

    class BodyParser(parsers.BodyParser):

        request_uuid = parsers.UUIDField()

    @command(
        name=name.Create('AUTH_TOKEN'),

        meta=Meta(
            title='Create Auth Token',
            domain=ACCOUNT_AUTHENTICATION),

        input=Input(body_parser=BodyParser),

        output=Output(serializer=AuthTokenSerializer),
    )
    def post(self, request):

        r = AuthRequest.objects.get(
            uuid=request.input.body['request_uuid'],
            account__isnull=False)

        raise self.event.Created({'token': r.get_token_and_delete()})