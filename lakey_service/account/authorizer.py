
from lily import BaseAuthorizer
from django.http import HttpResponseForbidden

from .token import AuthToken


class Authorizer(BaseAuthorizer):

    def __init__(self, access_list):
        self.access_list = access_list

    def authorize(self, request):

        try:
            type_, token = request.META['HTTP_AUTHORIZATION'].split()

        except KeyError:
            raise self.AuthError('COULD_NOT_FIND_AUTH_TOKEN')

        else:
            if type_.lower().strip() != 'bearer':
                raise self.AuthError('COULD_NOT_FIND_AUTH_TOKEN')

        account = AuthToken.decode(token)

        if account.type not in self.access_list:
            raise self.AccessDenied('ACCESS_DENIED')

        # -- return the enrichment that should be available as
        # -- `request.access` attribute
        return {'account': account}

    # FIXME: this is a temporary solution just to make it work
    # while the UI is still handled by django
    def ui_authorize(self, request):

        try:
            token = request.COOKIES['lakey-auth-token']

        except KeyError:
            raise HttpResponseForbidden('NO_AUTH_TOKEN_DETECTED')

        account = AuthToken.decode(token)

        return account

    def log(self, authorize_data):
        return {
            'account_id': authorize_data['account'].id
        }
