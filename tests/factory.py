
# from datetime import datetime
# from random import choice

from faker import Faker
# from django.utils import timezone

from account.models import (
    Account,
    AuthRequest,
)


faker = Faker()


class EntityFactory:

    def clear(self, with_predefined=True):
        Account.objects.all().delete()
        AuthRequest.objects.all().delete()

    def account(self, email=None, type=None):
        return Account.objects.create(
            email=email or faker.email(),
            type=type or Account.TYPES.RESEARCHER)

    def auth_request(self, account=None):

        r = AuthRequest.objects.create()

        if account:
            r.account = account
            r.save()

        return r

    def catalogue_item(self, name):
        pass
