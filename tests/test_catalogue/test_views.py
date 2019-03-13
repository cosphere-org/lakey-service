
import json

from django.test import TestCase
from django.urls import reverse
from lily.base.test import Client
import pytest

from account.models import Account
from account.token import AuthToken
from catalogue.models import CatalogueItem
from catalogue.serializers import CatalogueItemSerializer
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemCollectionViewTestCase(TestCase):

    uri = reverse('catalogue:items.collection')

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=Account.TYPES.ADMIN)

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
            'user_id': 'anonymous',
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
            'user_id': 'anonymous',
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
        ci_1 = ef.catalogue_item(name='temperatures')
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


class CatalogueItemElementViewTestCase(TestCase):

    def get_uri(self, item_id):
        return reverse('catalogue:items.element', kwargs={'item_id': item_id})

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=Account.TYPES.ADMIN)

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
            'user_id': 'anonymous',
        }

    #
    # UPDATE
    #
    def test_put_200(self):

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
                        'type': 'FLOAT',
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

        assert response.status_code == 200
        ci.refresh_from_db()
        assert response.json() == {
            '@event': 'CATALOGUEITEM_UPDATED',
            **CatalogueItemSerializer(ci).data
        }
        assert ci.name == 'iot_events'
        assert ci.spec == [
            {
                'name': 'value',
                'type': 'FLOAT',
                'size': 19203,
                'is_nullable': False,
                'distribution': None,
            },
        ]
        assert ci.maintained_by == a
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
            'user_id': 'anonymous',
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
            'user_id': 'anonymous',
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

    def test_delete_404(self):

        response = self.app.delete(
            self.get_uri(69506),
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_CATALOGUEITEM',
            '@type': 'error',
            'user_id': 'anonymous',
        }
