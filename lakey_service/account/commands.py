
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

        # FIXME: !!!! fix this URL!!!
        # - make it absolute
        # - make it add query param
        raise self.event.Created({
            # 'authenticate_ui_uri': reverse(
            #     'account:auth.requests.authenticate.ui',
            #     kwargs={'request_uuid': r.uuid}),
            'request_uuid': r.uuid,
        })


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


class AuthRequestAuthTokenCommands(HTTPCommands):

    class BodyParser(parsers.Parser):

        request_uuid = parsers.UUIDField()

    @command(
        name=name.Create('AUTH_TOKEN_FOR_AUTH_REQUEST'),

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


class AuthTokenCommands(HTTPCommands):

    class BodyParser(parsers.Parser):

        oauth_token = parsers.CharField()

        email = parsers.EmailField()

    @command(
        name=name.Create('AUTH_TOKEN'),

        meta=Meta(
            title='Generate Token',
            domain=ACCOUNT_AUTHENTICATION),

        input=Input(body_parser=BodyParser),

        output=Output(serializer=AuthTokenSerializer),
    )
    def post(self, request):

        email = request.input.body['email']

        oauth_token = request.input.body['oauth_token']

        account = Account.objects.get_or_create_oauth2(email, oauth_token)

        raise self.event.Created({'token': AuthToken.encode(account)})
