
import uuid

from django.utils import timezone
from django.db import models
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from lily.base.events import EventFactory
from lily.base.models import EnumChoiceField

from .token import AuthToken


class Account(models.Model):

    email = models.EmailField(unique=True)

    class AccountType:

        RESEARCHER = 'RESEARCHER'

        ADMIN = 'ADMIN'

        ANY = [RESEARCHER, ADMIN]

    type = EnumChoiceField(
        max_length=64,
        default=AccountType.RESEARCHER,
        enum_name='account_type',
        choices=[(t, t) for t in AccountType.ANY])

    def __str__(self):
        return self.email


class AuthRequest(models.Model):

    #
    # Version Control
    #
    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

    #
    # Authorship
    #
    account = models.ForeignKey(
        Account,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    #
    # Model Specific Fields
    #
    uuid = models.UUIDField(
        default=uuid.uuid1,
        editable=False)

    def attach_account(self, email, oauth_token):

        if self.get_oauth2_email(oauth_token) != email:
            raise EventFactory.BrokenRequest('EMAIL_MISMATCH_DETECTED')

        self.account, _ = Account.objects.get_or_create(email=email)
        self.save()

    def get_oauth2_email(self, oauth_token):

        try:
            idinfo = id_token.verify_oauth2_token(
                oauth_token,
                requests.Request(),
                settings.GOOGLE_OAUTH2_CLIENT_ID)

            issuers = ['accounts.google.com', 'https://accounts.google.com']
            if idinfo['iss'] not in issuers:
                raise EventFactory.Conflict(
                    'GOOGLE_OAUTH2_USER_INFO_ERROR_DETECTED')

            return idinfo['email']

        except ValueError:
            raise EventFactory.Conflict(
                'GOOGLE_OAUTH2_USER_INFO_ERROR_DETECTED')

    @property
    def expired(self):

        max_dt = settings.AUTH_REQUEST_EXPIRATION_DELTA
        actual_dt = timezone.now() - self.created_datetime

        return actual_dt > max_dt

    def get_token_and_delete(self):

        if not self.expired:
            token = AuthToken.encode(self.account)
            self.delete()

            return token

        else:
            raise EventFactory.BrokenRequest(
                'EXPIRED_AUTH_REQUEST_DETECTED')
