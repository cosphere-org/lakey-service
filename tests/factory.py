
from random import choice

from faker import Faker

from account.models import (
    Account,
    AuthRequest,
)
from catalogue.models import CatalogueItem

faker = Faker()


class EntityFactory:

    def clear(self, with_predefined=True):
        Account.objects.all().delete()
        AuthRequest.objects.all().delete()
        CatalogueItem.objects.all().delete()

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

    def catalogue_item(
            self,
            created_by=None,
            updated_by=None,
            maintained_by=None,
            name=None,
            sample=None,
            spec=None,
            executor_type=None):

        return CatalogueItem.objects.create(
            created_by=created_by,
            updated_by=updated_by,
            maintained_by=maintained_by,
            name=name or faker.name(),
            sample=sample or [],
            spec=spec or [
                {
                    'name': 'location',
                    'type': 'STRING',
                    'size': 190234,
                    'is_nullable': False,
                    'distribution': None,
                },
                {
                    'name': 'value',
                    'type': 'FLOAT',
                    'size': None,
                    'is_nullable': True,
                    'distribution': [
                        {'value': 18.0, 'count': 9},
                        {'value': 19.1, 'count': 45},
                        {'value': 21.2, 'count': 10},
                    ],
                },
            ],
            executor_type=executor_type or choice(['DATABRICKS', 'ATHENA']))
