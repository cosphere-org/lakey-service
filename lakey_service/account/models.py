
import uuid

from django.utils import timezone
from django.db import models
from django.conf import settings
from requests_oauthlib import OAuth2Session
from lily.base.events import EventFactory

from .token import AuthToken
from .constants import ACCOUNT_TYPE_ANY, ACCOUNT_TYPE_RESEARCHER


class Account(models.Model):

    email = models.EmailField(unique=True)

    type = models.CharField(
        max_length=64,
        default=ACCOUNT_TYPE_RESEARCHER,
        choices=[(t, t) for t in ACCOUNT_TYPE_ANY])


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

    def attach_account(self, email, authorization_code):

        if self.get_oauth2_email(authorization_code) != email:
            raise EventFactory.BrokenRequest('EMAIL_MISMATCH_DETECTED')

        self.account, _ = Account.objects.get_or_create(email=email)
        self.save()

    def get_oauth2_email(self, authorization_code):

        session = OAuth2Session(
            settings.GOOGLE_OAUTH2_CLIENT_ID,
            scope=settings.GOOGLE_OAUTH2_SCOPE)

        session.fetch_token(
            settings.GOOGLE_OAUTH2_TOKEN_URI,
            code=authorization_code,
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET)

        response = session.get(settings.GOOGLE_OAUTH2_USER_INFO_URI)
        if response.status_code == 200:
            return response.json()['email']

        else:
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
