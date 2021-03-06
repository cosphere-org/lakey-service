
from django.test import TestCase

from downloader.serializers import (
    DownloadRequestEstimateSerializer,
    DownloadRequestSerializer,
    DownloadRequestListSerializer,
)
from account.serializers import AccountSerializer
from catalogue.serializers import CatalogueItemSerializer
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestEstimateSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        assert DownloadRequestEstimateSerializer({
            'estimated_size': 5869,
        }).data == {
            '@type': 'download_request_estimated_size',
            'estimated_size': 5869,
        }


class DownloadRequestSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        a = ef.account()
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

        r = ef.download_request(
            created_by=a,
            spec={
                'columns': ['product'],
                'filters': [
                    {
                        'name': 'price',
                        'operator': '>=',
                        'value': 120,
                    },
                ],
                'randomize_ratio': 0.9,
            },
            blob_name=None,
            real_size=1829,
            estimated_size=1933,
            catalogue_item=ci,
            executor_job_id='fd90-fd89')

        assert DownloadRequestSerializer(r).data == {
            '@type': 'download_request',
            'created_by': AccountSerializer(a).data,
            'spec': {
                'columns': ['product'],
                'filters': [
                    {
                        'name': 'price',
                        'operator': '>=',
                        'value': 120,
                    },
                ],
                'randomize_ratio': 0.9,
            },
            'blob_name': None,
            'download_uri': None,
            'real_size': 1829,
            'estimated_size': 1933,
            'catalogue_item': CatalogueItemSerializer(ci).data,
            'executor_job_id': 'fd90-fd89',
            'is_cancelled': False,
        }


class DownloadRequestListSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        a_0 = ef.account()
        a_1 = ef.account()

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

        r_0 = ef.download_request(
            created_by=a_0,
            spec={
                'columns': ['product'],
                'filters': [
                    {
                        'name': 'price',
                        'operator': '>=',
                        'value': 120,
                    },
                ],
                'randomize_ratio': 0.9,
            },
            blob_name=None,
            real_size=1829,
            estimated_size=1933,
            catalogue_item=ci,
            executor_job_id='fd90-fd89')
        r_1 = ef.download_request(
            created_by=a_1,
            spec={
                'columns': ['price', 'product'],
                'filters': [],
                'randomize_ratio': 1,
            },
            blob_name=None,
            real_size=1829,
            estimated_size=1933,
            catalogue_item=ci,
            executor_job_id='fd90-fd89')

        assert DownloadRequestListSerializer({
            'requests': [r_0, r_1]
        }).data == {
            '@type': 'download_requests_list',
            'requests': [
                DownloadRequestSerializer(r_0).data,
                DownloadRequestSerializer(r_1).data,
            ],
        }
