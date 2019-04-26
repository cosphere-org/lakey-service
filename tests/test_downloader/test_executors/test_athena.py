
from django.test import TestCase

from downloader.models import DownloadRequest
from downloader.executors.athena import AthenaExecutor
from tests.factory import EntityFactory


ef = EntityFactory()


class AthenaExecutorTestCase(TestCase):

    def setUp(self):
        ef.clear()

        self.executor = AthenaExecutor()

        self.ci = ef.catalogue_item(
            name='lakey.shopping',
            spec=[
                {
                    'name': 'product',
                    'type': 'STRING',
                    'is_nullable': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'quantity',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'available',
                    'type': 'BOOLEAN',
                    'is_nullable': False,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'price',
                    'type': 'FLOAT',
                    'is_nullable': False,
                    'size': None,
                    'distribution': None,
                },
            ])

    #
    # COMPILE_TO_QUERY
    #
    def test_compile_to_query__columns_select(self):

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product', 'available'],
                'filters': [],
            },
            catalogue_item=self.ci)

        assert self.executor.compile_to_query(d) == (
            'SELECT product, available FROM lakey.shopping')

    def test_compile_to_query__numerical_filters(self):

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product', 'quantity'],
                'filters': [
                    {
                        'name': 'price',
                        'operator': '>=',
                        'value': 78.1,
                    },
                ],
            },
            catalogue_item=self.ci)

        assert self.executor.compile_to_query(d) == (
            'SELECT product, quantity FROM lakey.shopping '
            'WHERE price >= 78.1')

    def test_compile_to_query__categorical_filters(self):

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product', 'quantity'],
                'filters': [
                    {
                        'name': 'product',
                        'operator': '=',
                        'value': 'jeans',
                    },
                ],
            },
            catalogue_item=self.ci)

        assert self.executor.compile_to_query(d) == (
            'SELECT product, quantity FROM lakey.shopping '
            'WHERE product = \'jeans\'')

    def test_compile_to_query__many_filters(self):

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product', 'available'],
                'filters': [
                    {
                        'name': 'price',
                        'operator': '>=',
                        'value': 289.2,
                    },
                    {
                        'name': 'product',
                        'operator': '=',
                        'value': 'jeans',
                    },
                ],
            },
            catalogue_item=self.ci)

        assert self.executor.compile_to_query(d) == (
            'SELECT product, available FROM lakey.shopping '
            'WHERE price >= 289.2 AND product = \'jeans\'')

    def test_compile_to_query__radomization_filters(self):

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product', 'available'],
                'filters': [],
                'randomize_ratio': 0.9,
            },
            catalogue_item=self.ci)

        assert self.executor.compile_to_query(d) == (
            'SELECT product, available FROM lakey.shopping '
            'WHERE RAND() >= 0.9')
