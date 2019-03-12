
from lily.base.events import EventFactory

from .token import AuthToken


class Authorizer:

    def __init__(self, access_list):
        self.access_list = access_list

    def authorize(self, request):

        try:
            type_, token = request.META['HTTP_AUTHORIZATION'].split()

        except KeyError:
            raise EventFactory.AuthError('COULD_NOT_FIND_AUTH_TOKEN')

        else:
            if type_ != 'bearer':
                raise EventFactory.AuthError('COULD_NOT_FIND_AUTH_TOKEN')

        account = AuthToken.decode(token)

        if account.type not in self.access_list:
            raise EventFactory.AccessDenied('ACCESS_DENIED')

        request.account = account
