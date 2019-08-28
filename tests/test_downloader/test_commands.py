
import json

from django.test import TestCase
from django.urls import reverse
from lily.base.test import Client
import pytest

from account.models import Account
from account.token import AuthToken
from downloader.models import DownloadRequest
from downloader.serializers import DownloadRequestSerializer
from downloader.executors.athena import AthenaExecutor
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestRenderCommandsTestCase(TestCase):

    uri = reverse('downloader:requests.render_ui_data')

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=Account.AccountType.ADMIN)

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'  # noqa
        }

    def test_post_200(self):

        ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'product',
                    'type': 'STRING',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'price',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'available',
                    'type': 'BOOLEAN',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                }
            ])

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'catalogue_item_id': ci.id,
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'DOWNLOAD_REQUEST_UI_DATA_RENDERED',
            '@type': 'download_request_render',
            'columns_operators': [
                {
                    '@type': 'column_operators',
                    'name': 'available',
                    'operators': ['=', '!='],
                },
                {
                    '@type': 'column_operators',
                    'name': 'price',
                    'operators': ['>', '>=', '<', '<=', '=', '!='],
                },
                {
                    '@type': 'column_operators',
                    'name': 'product',
                    'operators': ['>', '>=', '<', '<=', '=', '!='],
                },
            ],
        }


class DownloadRequestEstimateCommandsTestCase(TestCase):

    uri = reverse('downloader:requests.estimate')

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=Account.AccountType.ADMIN)

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def test_post_200(self):

        estimate_size = self.mocker.patch.object(
            DownloadRequest.objects, 'estimate_size')
        estimate_size.return_value = 1234
        ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'product',
                    'type': 'STRING',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'price',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                },
            ])

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'spec': {
                    'columns': ['product', 'price'],
                    'filters': [],
                    'randomize_ratio': 0.9,
                },
                'catalogue_item_id': ci.id,
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'SIZE_OF_DOWNLOAD_REQUEST_ESTIMATED',
            '@type': 'download_request_estimated_size',
            'estimated_size': 1234,
        }


class DownloadRequestCollectionCommandsTestCase(TestCase):

    uri = reverse('downloader:requests.collection')

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=Account.AccountType.ADMIN)
        self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'product',
                    'type': 'STRING',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'price',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                },
            ])

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    #
    # CREATE DOWNLOAD REQUEST
    #
    def test_post_201__created(self):

        execute = self.mocker.patch.object(AthenaExecutor, 'execute')
        execute.return_value = (
            'https://s3.this.region.amazonaws.com/buk.et/results/567.csv')
        assert DownloadRequest.objects.all().count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'spec': {
                    'columns': ['product', 'price'],
                    'filters': [
                        {'name': 'price', 'operator': '>=', 'value': 78},
                    ],
                    'randomize_ratio': 0.9,
                },
                'catalogue_item_id': self.ci.id,
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 201
        assert DownloadRequest.objects.all().count() == 1
        r = DownloadRequest.objects.all().first()

        assert response.json() == {
            '@event': 'DOWNLOADREQUEST_CREATED',
            **DownloadRequestSerializer(r).data,
        }
        assert r.created_by == self.account

    def test_post_200__read(self):

        execute = self.mocker.patch.object(AthenaExecutor, 'execute')

        r = ef.download_request(
            spec={
                'columns': ['price', 'product'],
                'filters': [
                    {'name': 'price', 'operator': '>=', 'value': 78},
                    {'name': 'price', 'operator': '=', 'value': 23},
                    {'name': 'product', 'operator': '=', 'value': 'jack'},
                ],
                'randomize_ratio': 0.9,
            },
            uri=(
                'https://s3.this.region.amazonaws.com/buk.et/results/567.csv'),
            catalogue_item=self.ci)

        assert DownloadRequest.objects.all().count() == 1

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'spec': {
                    'columns': ['product', 'price'],
                    'filters': [
                        {'name': 'product', 'operator': '=', 'value': 'jack'},
                        {'name': 'price', 'operator': '=', 'value': 23},
                        {'name': 'price', 'operator': '>=', 'value': 78},
                    ],
                    'randomize_ratio': 0.9,
                },
                'catalogue_item_id': self.ci.id,
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 200
        assert DownloadRequest.objects.all().count() == 1
        assert DownloadRequest.objects.all().first() == r

        assert response.json() == {
            '@event': 'DOWNLOADREQUEST_READ',
            **DownloadRequestSerializer(r).data,
        }
        assert execute.call_count == 0

    def test_post_400__broken_request(self):

        assert DownloadRequest.objects.all().count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'spec': {
                    'columns': ['product', 'price'],
                    'filters': [],
                    'randomize_ratio': 0.9,
                },
                'catalogue_item_id': 'TEXT',
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 400
        assert DownloadRequest.objects.all().count() == 0
        assert response.json() == {
            '@event': 'BODY_DID_NOT_VALIDATE',
            '@type': 'error',
            'errors': {
                'catalogue_item_id': ['A valid integer is required.'],
            },
            '@access': {
                'account_id': self.account.id,
            },
        }

    def test_post_404__catalogue_item_does_not_exist(self):

        assert DownloadRequest.objects.all().count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'spec': {
                    'columns': ['product', 'price'],
                    'filters': [],
                    'randomize_ratio': 0.9,
                },
                'catalogue_item_id': 58495,
            }),
            content_type='application/json',
            **self.headers)

        assert response.status_code == 404
        assert DownloadRequest.objects.all().count() == 0
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_CATALOGUEITEM',
            '@type': 'error',
            '@access': {'account_id': self.account.id},
        }

    #
    # BULK READ DOWNLOAD REQUESTS
    #
    def test_get_200(self):

        a = ef.account()
        d_0 = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product'],
                'filters': [{'name': 'price', 'operator': '>=', 'value': 78}],
                'randomize_ratio': 1,
            },
            catalogue_item=self.ci)
        d_0.waiters.add(self.account)

        d_1 = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product'],
                'filters': [{'name': 'price', 'operator': '=', 'value': 18}],
                'randomize_ratio': 0.8,
            },
            catalogue_item=self.ci)
        d_1.waiters.add(self.account)

        # -- noise
        d_2 = DownloadRequest.objects.create(  # noqa
            created_by=a,
            spec={
                'columns': ['price'],
                'filters': [],
                'randomize_ratio': 0.1,
            },
            catalogue_item=self.ci)

        response = self.app.get(
            self.uri,
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'DOWNLOADREQUESTS_BULK_READ',
            '@type': 'download_requests_list',
            'requests': [
                DownloadRequestSerializer(d_0).data,
                DownloadRequestSerializer(d_1).data,
            ],
        }


class DownloadRequestElementCommandsTestCase(TestCase):

    def get_uri(self, request_id):
        return reverse(
            'downloader:requests.element', kwargs={'request_id': request_id})

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=Account.AccountType.ADMIN)

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

        self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'product',
                    'type': 'STRING',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'price',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                },
            ])

    #
    # READ
    #
    def test_get_200(self):

        d = DownloadRequest.objects.create(
            created_by=ef.account(),
            spec={
                'columns': ['product'],
                'filters': [{'name': 'price', 'operator': '>=', 'value': 78}],
                'randomize_ratio': 1,
            },
            catalogue_item=self.ci)
        d.waiters.add(self.account)

        response = self.app.get(
            self.get_uri(d.id),
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'DOWNLOADREQUEST_READ',
            **DownloadRequestSerializer(d).data,
        }

    def test_get_404__wrong_user(self):

        d = DownloadRequest.objects.create(
            created_by=ef.account(),
            spec={
                'columns': ['product'],
                'filters': [{'name': 'price', 'operator': '>=', 'value': 78}],
                'randomize_ratio': 1,
            },
            catalogue_item=self.ci)

        response = self.app.get(
            self.get_uri(d.id),
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_DOWNLOADREQUEST',
            '@type': 'error',
            '@access': {
                'account_id': self.account.id,
            },
        }

    def test_get_404__wrong_id(self):

        response = self.app.get(
            self.get_uri(69506),
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_DOWNLOADREQUEST',
            '@type': 'error',
            '@access': {
                'account_id': self.account.id,
            },
        }

    #
    # DELETE
    #
    def test_delete_200(self):

        d = DownloadRequest.objects.create(
            created_by=ef.account(),
            spec={
                'columns': ['product'],
                'filters': [{'name': 'price', 'operator': '>=', 'value': 78}],
                'randomize_ratio': 1,
            },
            is_cancelled=False,
            catalogue_item=self.ci)
        d.waiters.add(self.account)
        assert DownloadRequest.objects.all().count() == 1

        response = self.app.delete(
            self.get_uri(d.id),
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'DOWNLOADREQUEST_DELETED',
            '@type': 'empty',
        }
        assert DownloadRequest.objects.all().count() == 1
        d.refresh_from_db()
        assert d.waiters.count() == 0
        assert d.is_cancelled is True

    def test_delete_404(self):

        response = self.app.delete(
            self.get_uri(69506),
            **self.headers)

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_DOWNLOADREQUEST',
            '@type': 'error',
            '@access': {
                'account_id': self.account.id,
            },
        }
