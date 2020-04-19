
from enum import Enum, unique
import uuid

from django.db import models, IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from lily.base.events import EventFactory
from lily.base.models import EnumChoiceField

from .token import AuthToken


def validate_token(email, oauth_token):

    try:
        idinfo = id_token.verify_oauth2_token(
            oauth_token,
            requests.Request(),
            settings.GOOGLE_OAUTH2_CLIENT_ID)

        issuers = ['accounts.google.com', 'https://accounts.google.com']
        if idinfo['iss'] not in issuers:
            raise EventFactory.Conflict(
                'GOOGLE_OAUTH2_USER_INFO_ERROR_DETECTED')

        gmail_email = idinfo['email']

    except ValueError:
        raise EventFactory.Conflict(
            'GOOGLE_OAUTH2_USER_INFO_ERROR_DETECTED')

    # -- validate email
    if gmail_email != email:
        raise EventFactory.BrokenRequest('EMAIL_MISMATCH_DETECTED')

    # -- validate domain
    domain = email.split('@')[1]
    if domain not in settings.GOOGLE_OAUTH2_ALLOWED_DOMAINS:
        raise EventFactory.AuthError('WRONG_EMAIL_DOMAIN')

    return gmail_email


@unique
class AccountType(Enum):

    RESEARCHER = 'RESEARCHER'

    ADMIN = 'ADMIN'


class AccountManager(models.Manager):

    def get_or_create_oauth2(self, email, oauth_token):

        validate_token(email, oauth_token)

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=None)

        except IntegrityError:
            user = User.objects.get(username=email, email=email)

        account, _ = Account.objects.get_or_create(
            email=email, user=user)

        return account


class Account(models.Model):

    objects = AccountManager()

    email = models.EmailField(unique=True)

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    type = EnumChoiceField(enum=AccountType)

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

        validate_token(email, oauth_token)

        self.account, _ = Account.objects.get_or_create(email=email)
        self.save()

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
