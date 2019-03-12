
from datetime import datetime

from django.conf import settings
import jwt
from lily.base.events import EventFactory


class AuthToken:

    @staticmethod
    def encode(account):

        return jwt.encode(
            AuthToken.get_payload(account),
            settings.AUTH_TOKEN_SECRET_KEY,
            settings.AUTH_TOKEN_ALGORITHM
        ).decode('utf-8')

    @staticmethod
    def get_payload(account):

        return {
            'id': account.id,
            'email': account.email,
            'type': account.type,
            'exp': datetime.utcnow() + settings.AUTH_TOKEN_EXPIRATION_DELTA
        }

    @staticmethod
    def decode(token):

        # -- token decode
        try:
            payload = jwt.decode(
                token,
                settings.AUTH_TOKEN_SECRET_KEY,
                True,
                options={'verify_exp': True})

        except jwt.ExpiredSignature:
            raise EventFactory.AuthError('AUTH_TOKEN_EXPIRED')

        except jwt.DecodeError:
            raise EventFactory.AuthError('AUTH_TOKEN_WAS_BROKEN')

        # -- payload decode
        try:
            account_id = payload['id']
            account_email = payload['email']
            account_type = payload['type']

        except KeyError:
            raise EventFactory.AuthError(
                'AUTH_TOKEN_MISSING_FIELDS_DETECTED')

        # -- payload to account
        from account.models import Account  # -- avoid cyclic imports

        # -- make sure that account exists
        try:
            return Account.objects.get(
                id=account_id,
                email=account_email,
                type=account_type)

        except Account.DoesNotExist:
            raise EventFactory.AuthError(
                'AUTH_TOKEN_MISSING_ACCOUNT')
