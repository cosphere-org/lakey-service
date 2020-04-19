
import json

from django.test import TestCase
from django.urls import reverse
from lily.base.test import Client
import pytest

from account.models import AccountType
from account.token import AuthToken
from catalogue.models import CatalogueItem
from catalogue.serializers import CatalogueItemSerializer
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemCollectionCommandsTestCase(TestCase):

    uri = reverse('catalogue:items.collection')

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=AccountType.ADMIN.value)

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    #
    # CREATE CATALOGUE ITEM
    #
    def test_post_201(self):

        a = ef.account()

        assert CatalogueItem.objects.all().count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'name': 'iot_events',
                'sample': [],
                'spec': [
                    {
                        'name': 'value',
                        'type': 'FLOAT',
                        'size': 19203,
                        'is_nullable': False,
                        'is_enum': False,
                        'distribution': None,
                    },
                ],
                'maintained_by_id': a.id,
                'executor_type': 'DATABRICKS',
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 201
        assert CatalogueItem.objects.all().count() == 1
        ci = CatalogueItem.objects.all().first()

        assert response.json() == {
            '@event': 'CATALOGUEITEM_CREATED',
            **CatalogueItemSerializer(ci).data,
        }
        assert ci.created_by == self.account
        assert ci.updated_by == self.account

    def test_post_400__broken_request(self):

        a = ef.account()

        assert CatalogueItem.objects.all().count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'name': 'iot_events',
                'sample': [],
                'spec': [
                    {
                        'name': 'value',
                        'size': 19203,
                        'is_nullable': False,
                        'distribution': None,
                    },
                ],
                'maintained_by_id': a.id,
                'executor_type': 'DATABRICKS',
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 400
        assert CatalogueItem.objects.all().count() == 0
        assert response.json() == {
            '@event': 'BODY_DID_NOT_VALIDATE',
            '@type': 'error',
            'errors': {
                'spec': [
                    "JSON did not validate. PATH: '0' REASON: 'type' is a "
                    "required property",
                ],
            },
            '@authorizer': {
                'account_id': self.account.id,
            },
        }

    def test_post_400__maintainer_does_not_exist(self):

        assert CatalogueItem.objects.all().count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'name': 'iot_events',
                'sample': [],
                'spec': [
                    {
                        'name': 'value',
                        'type': 'FLOAT',
                        'size': 19203,
                        'is_nullable': False,
                        'is_enum': False,
                        'distribution': None,
                    },
                ],
                'maintained_by_id': 932039,
                'executor_type': 'DATABRICKS',
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 400
        assert CatalogueItem.objects.all().count() == 0
        assert response.json() == {
            'errors': {
                'maintained_by': [
                    'account instance with id 932039 does not exist.'],
            },
            '@authorizer': {
                'account_id': self.account.id,
            },
            '@type': 'error',
            '@event': 'BODY_JSON_DID_NOT_PARSE',
        }

    #
    # BULK READ CATALOGUE ITEMS
    #
    def test_get_200(self):

        ci_0 = ef.catalogue_item(name='iot_features')
        ci_1 = ef.catalogue_item(name='iot_events')
        ci_2 = ef.catalogue_item(name='temperatures')

        response = self.app.get(
            self.uri,
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEMS_BULK_READ',
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_0).data,
                CatalogueItemSerializer(ci_1).data,
                CatalogueItemSerializer(ci_2).data,
            ],
        }

    def test_get_200__with_query(self):

        ci_0 = ef.catalogue_item(name='iot_features')
        ci_1 = ef.catalogue_item(name='temperatures')  # noqa
        ci_2 = ef.catalogue_item(name='iot_events')

        response = self.app.get(
            self.uri,
            data={'query': 'IoT'},
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEMS_BULK_READ',
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_0).data,
                CatalogueItemSerializer(ci_2).data,
            ],
        }

    def test_get_200__query_many_words_default(self):

        ci_0 = ef.catalogue_item(name='iot_features')
        ci_1 = ef.catalogue_item(name='temperatures')  # noqa
        ci_2 = ef.catalogue_item(name='iot_events')  # noqa

        response = self.app.get(
            self.uri,
            data={'query': 'feature tempera'},
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEMS_BULK_READ',
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_0).data,
                CatalogueItemSerializer(ci_1).data,
            ],
        }

    def test_get_200__query_many_words_and_or(self):

        ci_0 = ef.catalogue_item(name='iot_features')
        ci_1 = ef.catalogue_item(name='temperatures')  # noqa
        ci_2 = ef.catalogue_item(name='iot_events')  # noqa

        response = self.app.get(
            self.uri,
            data={'query': 'feature & IOT | temperature'},
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEMS_BULK_READ',
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_0).data,
                CatalogueItemSerializer(ci_1).data,
            ],
        }

    def test_get_200__query_many_words_or_not(self):

        ci_0 = ef.catalogue_item(name='iot_features')  # noqa
        ci_1 = ef.catalogue_item(name='temperatures')  # noqa
        ci_2 = ef.catalogue_item(name='iot_events')

        response = self.app.get(
            self.uri,
            data={'query': 'IOT ~features | temp'},
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEMS_BULK_READ',
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_1).data,
                CatalogueItemSerializer(ci_2).data,
            ],
        }

    def test_get_200__with_has_samples(self):

        ci_0 = ef.catalogue_item(name='iot_features', sample=[])
        ci_1 = ef.catalogue_item(
            name='temperatures',
            sample=[
                {'location': 'Wroclaw', 'value': 12.1},
                {'location': 'Olawa', 'value': 34.4},
            ])
        ci_2 = ef.catalogue_item(name='iot_events', sample=[])

        # -- with samples
        response = self.app.get(
            self.uri,
            data={'has_samples': True},
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEMS_BULK_READ',
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_1).data,
            ],
        }

        # -- without samples
        response = self.app.get(
            self.uri,
            data={'has_samples': False},
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEMS_BULK_READ',
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_0).data,
                CatalogueItemSerializer(ci_2).data,
            ],
        }


class CatalogueItemElementCommandsTestCase(TestCase):

    def get_uri(self, item_id):
        return reverse('catalogue:items.element', kwargs={'item_id': item_id})

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=AccountType.ADMIN.value)

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    #
    # READ
    #
    def test_get_200(self):

        ci_0 = ef.catalogue_item(name='temperatures')
        # -- noise
        ci_1 = ef.catalogue_item(name='iot_features')  # noqa

        response = self.app.get(
            self.get_uri(ci_0.id),
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEM_READ',
            **CatalogueItemSerializer(ci_0).data,
        }

    def test_get_404(self):

        response = self.app.get(
            self.get_uri(69506),
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_CATALOGUEITEM',
            '@type': 'error',
            '@authorizer': {
                'account_id': self.account.id,
            },
        }

    #
    # UPDATE
    #
    def test_put_200(self):

        a_0 = ef.account()
        a_1 = ef.account()
        ci = ef.catalogue_item(
            name='temperatures',
            created_by=a_1,
            updated_by=a_1)

        response = self.app.put(
            self.get_uri(ci.id),
            data=json.dumps({
                'sample': [],
                'spec': [
                    {
                        'name': 'value',
                        'type': 'FLOAT',
                        'size': 19203,
                        'is_nullable': False,
                        'is_enum': False,
                        'distribution': None,
                    },
                ],
                'maintained_by_id': a_0.id,
                'executor_type': 'DATABRICKS',
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 200
        ci.refresh_from_db()
        assert response.json() == {
            '@event': 'CATALOGUEITEM_UPDATED',
            **CatalogueItemSerializer(ci).data
        }
        assert ci.name == 'temperatures'
        assert ci.spec == [
            {
                'name': 'value',
                'type': 'FLOAT',
                'size': 19203,
                'is_nullable': False,
                'is_enum': False,
                'distribution': None,
            },
        ]
        assert ci.maintained_by == a_0
        assert ci.created_by == a_1
        assert ci.updated_by == self.account
        assert ci.executor_type == 'DATABRICKS'

    def test_put_400(self):

        a = ef.account()
        ci = ef.catalogue_item(name='temperatures')

        response = self.app.put(
            self.get_uri(ci.id),
            data=json.dumps({
                'name': 'iot_events',
                'sample': [],
                'spec': [
                    {
                        'name': 'value',
                        'size': 19203,
                        'is_nullable': False,
                        'is_enum': False,
                        'distribution': None,
                    },
                ],
                'maintained_by_id': a.id,
                'executor_type': 'DATABRICKS',
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 400
        assert response.json() == {
            '@event': 'BODY_DID_NOT_VALIDATE',
            '@type': 'error',
            'errors': {
                'spec': [
                    "JSON did not validate. PATH: '0' REASON: 'type' is a "
                    "required property",
                ],
            },
            '@authorizer': {
                'account_id': self.account.id,
            },
        }

    def test_put_404(self):

        response = self.app.put(
            self.get_uri(9022),
            data=json.dumps({
                'name': 'iot_events',
                'sample': [],
                'spec': [
                    {
                        'name': 'value',
                        'type': 'FLOAT',
                        'size': 19203,
                        'is_nullable': False,
                        'is_enum': False,
                        'distribution': None,
                    },
                ],
                'maintained_by_id': ef.account().id,
                'executor_type': 'DATABRICKS',
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_CATALOGUEITEM',
            '@type': 'error',
            '@authorizer': {
                'account_id': self.account.id,
            },
        }

    #
    # DELETE
    #
    def test_delete_200(self):

        ci_0 = ef.catalogue_item(name='temperatures')
        # -- noise
        ci_1 = ef.catalogue_item(name='iot_features')  # noqa

        assert CatalogueItem.objects.all().count() == 2

        response = self.app.delete(
            self.get_uri(ci_0.id),
            **self.headers)

        assert CatalogueItem.objects.all().count() == 1
        assert response.status_code == 200
        assert response.json() == {
            '@event': 'CATALOGUEITEM_DELETED',
            '@type': 'empty',
        }

    def test_delete_400__not_cancelled_download_requests(self):

        ci_0 = ef.catalogue_item(
            name='temperatures',
            spec=[
                {
                    'name': 'price',
                    'type': 'INTEGER',
                    'is_nullable': True,
                    'is_enum': True,
                    'distribution': None,
                    'size': 1920,
                },
            ])
        ef.download_request(
            spec={
                'columns': ['price'],
                'filters': [],
                'randomize_ratio': 0.1,
            },
            catalogue_item=ci_0)
        ef.download_request(
            spec={
                'columns': ['price'],
                'filters': [],
                'randomize_ratio': 0.2,
            },
            catalogue_item=ci_0, is_cancelled=True)

        # -- noise
        ci_1 = ef.catalogue_item(name='iot_features')  # noqa

        assert CatalogueItem.objects.all().count() == 2

        response = self.app.delete(
            self.get_uri(ci_0.id),
            **self.headers)

        assert CatalogueItem.objects.all().count() == 2
        assert response.status_code == 400
        assert response.json() == {
            '@authorizer': {'account_id': self.account.id},
            '@event': 'NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED',
            '@type': 'error',
            'item_id': ci_0.id,
            'not_cancelled_count': 1,
        }

    def test_delete_404(self):

        response = self.app.delete(
            self.get_uri(69506),
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_CATALOGUEITEM',
            '@type': 'error',
            '@authorizer': {
                'account_id': self.account.id,
            },
        }


class CatalogueItemSampleAndDistributionsCommandsTestCase(TestCase):

    def get_uri(self, item_id):
        return reverse(
            'catalogue:items.element.samples_and_distributions',
            kwargs={'item_id': item_id})

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=AccountType.ADMIN.value)

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    #
    # UPDATE
    #
    def test_put_200(self):

        update_samples_and_distributions = self.mocker.patch.object(
            CatalogueItem, 'update_samples_and_distributions')
        a_0 = ef.account()
        a_1 = ef.account()
        ci = ef.catalogue_item(
            name='temperatures',
            created_by=a_0,
            updated_by=a_1)

        response = self.app.put(
            self.get_uri(ci.id),
            **self.headers)

        assert response.status_code == 200
        ci.refresh_from_db()
        assert response.json() == {
            '@event': 'CATALOGUEITEM_WITH_SAMPLE_AND_DISTRIBUTION_UPDATED',
            '@type': 'empty',
        }
        assert update_samples_and_distributions.call_count == 1

    def test_put_404(self):

        response = self.app.put(
            self.get_uri(9022),
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_CATALOGUEITEM',
            '@type': 'error',
            '@authorizer': {
                'account_id': self.account.id,
            },
        }
