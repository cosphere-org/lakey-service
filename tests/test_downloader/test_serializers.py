
from django.test import TestCase

from downloader.serializers import (
    DownloadRequestRenderSerializer,
    DownloadRequestEstimateSerializer,
    DownloadRequestSerializer,
    DownloadRequestListSerializer,
)
from account.serializers import AccountSerializer
from chunk.serializers import ChunkSerializer
from catalogue.serializers import CatalogueItemSerializer
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestRenderSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        assert DownloadRequestRenderSerializer({
            'columns_operators': [
                {
                    'name': 'price',
                    'operators': ['>=', '='],
                },
                {
                    'name': 'available',
                    'operators': ['='],
                },
            ],
        }).data == {
            '@type': 'download_request_render',
            'columns_operators': [
                {
                    '@type': 'column_operators',
                    'name': 'price',
                    'operators': ['>=', '='],
                },
                {
                    '@type': 'column_operators',
                    'name': 'available',
                    'operators': ['='],
                },
            ],
        }


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
            uri=None,
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
            'uri': None,
            'real_size': 1829,
            'estimated_size': 1933,
            'catalogue_item': CatalogueItemSerializer(ci).data,
            'executor_job_id': 'fd90-fd89',
            'is_cancelled': False,
            'chunks': [],
        }

    def test_serialize__with_chunks(self):

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
            uri=None,
            real_size=1829,
            estimated_size=1933,
            catalogue_item=ci,
            executor_job_id='fd90-fd89')

        ch0 = ef.chunk(
            catalogue_item=ci,
            borders=[
                {
                    'column': 'product',
                    'minimum': 10,
                    'maximum': 15,
                    'distribution': None,
                },
                {
                    'column': 'price',
                    'minimum': 20,
                    'maximum': 25,
                    'distribution': None,
                },
            ],
            count=0)
        r.chunks.add(ch0)

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
            'uri': None,
            'real_size': 1829,
            'estimated_size': 1933,
            'catalogue_item': CatalogueItemSerializer(ci).data,
            'executor_job_id': 'fd90-fd89',
            'is_cancelled': False,
            'chunks': [
                ChunkSerializer(ch0).data,
            ],
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
            uri=None,
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
            uri=None,
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
