
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
    HTTPCommands,
)
from django.template.loader import render_to_string

from .domains import ACCOUNT_AUTHENTICATION
from .models import AuthRequest, Account
from .serializers import AuthTokenSerializer, AuthRequestSerializer
from .token import AuthToken


class AuthRequestCommands(HTTPCommands):

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
            'authenticate_ui_uri': reverse(
                'account:auth.requests.authenticate.ui',
                kwargs={'request_uuid': r.uuid}),
            'request_uuid': r.uuid,
        })


class AuthRequestAuthenticateUICommands(HTTPCommands):

    @command(
        name=name.Execute('RENDER', 'AUTH_REQUEST_AUTHENTICATE_UI'),

        meta=Meta(
            title='Render Auth Request Authentication UI',
            domain=ACCOUNT_AUTHENTICATION),
    )
    def get(self, request, request_uuid):

        # FIXME: check is such `request_uuid` exists!!!!
        return HttpResponse(render_to_string(
            'authenticate.html',
            {
                'auth_request_uuid': request_uuid,
                'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            }))


class AuthRequestAttachAccountCommands(HTTPCommands):

    class BodyParser(parsers.Parser):

        request_uuid = parsers.UUIDField()

        oauth_token = parsers.CharField()

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
            oauth_token=request.input.body['oauth_token'])

        raise self.event.Executed()


class AuthTokenCommands(HTTPCommands):

    class BodyParser(parsers.Parser):

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


class GetTokenUICommands(HTTPCommands):

    @command(
        name=name.Execute('RENDER', 'GET_TOKEN_UI'),

        meta=Meta(
            title='Get Token UI',
            domain=ACCOUNT_AUTHENTICATION),
    )
    def get(self, request):
        return HttpResponse(render_to_string(
            'get_token.html',
            {
                'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            }))


class GenerateTokenCommands(HTTPCommands):

    class BodyParser(parsers.Parser):

        oauth_token = parsers.CharField()

        email = parsers.EmailField()

    @command(
        name=name.Execute('GENERATE', 'TOKEN'),

        meta=Meta(
            title='Generate Token',
            domain=ACCOUNT_AUTHENTICATION),

        input=Input(body_parser=BodyParser),

        output=Output(serializer=serializers.ObjectSerializer),
    )
    def post(self, request):

        # validate google token
        gmail = AuthRequest.get_oauth2_email(request.input.body['oauth_token'])
        if request.input.body['email'] != gmail:
            raise self.event.BrokenRequest('EMAIL_MISMATCH_DETECTED')

        # validate domain
        domain = gmail.split('@')[1]
        if domain != 'viessmann.com':
            raise self.event.AuthError('WRONG_EMAIL_DOMAIN')

        # generate jwt token
        account, _ = Account.objects.get_or_create(email=gmail)
        token = AuthToken.encode(account)

        raise self.event.Executed({'token': token})
