
import re
from unittest.mock import Mock, call

from django.test import TestCase, override_settings
import httpretty
import pytest

from downloader.models import DownloadRequest
from downloader.executors.athena import AthenaExecutor
from tests.factory import EntityFactory


ef = EntityFactory()


def normalize_query(q):
    return re.sub(r'\s+', ' ', q).strip()


class AthenaExecutorTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

        self.mocker.patch('downloader.executors.athena.sleep')

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
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'quantity',
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
                },
                {
                    'name': 'price',
                    'type': 'FLOAT',
                    'is_nullable': False,
                    'is_enum': False,
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

        assert normalize_query(self.executor.compile_to_query(d)) == (
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

        assert normalize_query(self.executor.compile_to_query(d)) == (
            'SELECT q.* FROM ('
            'SELECT product, available FROM lakey.shopping ) '
            'AS q WHERE RAND() >= 0.9')

    #
    # GET_SAMPLE
    #
    @override_settings(
        CATALOGUE_ITEMS_SAMPLE_SIZE=17)
    def test_get_sample(self):

        execute_to_df = self.mocker.patch.object(
            AthenaExecutor, 'execute_to_df')
        execute_to_df.return_value = Mock(
            to_dict=Mock(return_value=[{'a': 1}, {'b': 3}]))

        assert self.executor.get_sample(self.ci) == [{'a': 1}, {'b': 3}]
        assert execute_to_df.call_count == 1
        database, query = execute_to_df.call_args

        assert database[0] == 'lakey'
        assert normalize_query(query['query']) == normalize_query(
            '''
            SELECT
                g.*
            FROM
                lakey.shopping AS g,
                (
                    SELECT
                        COUNT(*) AS total

                    FROM lakey.shopping
                ) as f
                WHERE rand() <= (1.2 * 17 / f.total)
                LIMIT 17
            ''')

    #
    # GET_SIZE
    #
    @override_settings(
        CATALOGUE_ITEMS_SAMPLE_SIZE=17)
    def test_get_size(self):

        execute_to_df = self.mocker.patch.object(
            AthenaExecutor, 'execute_to_df')
        execute_to_df.return_value = Mock(
            to_dict=Mock(return_value={'size': [5489]}))

        assert self.executor.get_size('email', self.ci) == 5489
        assert execute_to_df.call_count == 1
        database, query = execute_to_df.call_args

        assert database[0] == 'lakey'
        assert normalize_query(query['query']) == normalize_query(
            '''
            SELECT
                SUM(LENGTH(CAST(email AS VARCHAR))) AS size
            FROM
                lakey.shopping
            ''')

    #
    # GET_DISTRIBUTION
    #
    def test_get_distribution__enum(self):

        get_distribution_enum = self.mocker.patch.object(
            AthenaExecutor, 'get_distribution_enum')
        get_distribution_numerical = self.mocker.patch.object(
            AthenaExecutor, 'get_distribution_numerical')

        self.executor.get_distribution('price', 'INTEGER', True, self.ci)

        assert get_distribution_enum.call_args_list == [call('price', self.ci)]
        assert get_distribution_numerical.call_count == 0

    def test_get_distribution__numerical(self):

        get_distribution_enum = self.mocker.patch.object(
            AthenaExecutor, 'get_distribution_enum')
        get_distribution_numerical = self.mocker.patch.object(
            AthenaExecutor, 'get_distribution_numerical')

        self.executor.get_distribution('price', 'INTEGER', False, self.ci)

        assert get_distribution_enum.call_count == 0
        assert get_distribution_numerical.call_args_list == [
            call('price', self.ci),
        ]

    #
    # GET_DISTRIBUTION_ENUM
    #
    @override_settings(
        CATALOGUE_ITEMS_DISTRIBUTION_VALUE_LIMIT=123)
    def test_get_distribution_enum(self):

        execute_to_df = self.mocker.patch.object(
            AthenaExecutor, 'execute_to_df')
        execute_to_df.return_value = Mock(
            to_dict=Mock(return_value=[{'value': 'fun', 'count': 3}]))

        assert self.executor.get_distribution_enum(
            'product', self.ci) == [{'value': 'fun', 'count': 3}]
        assert execute_to_df.call_count == 1
        database, query = execute_to_df.call_args

        assert database[0] == 'lakey'
        assert normalize_query(query['query']) == normalize_query(
            '''
            SELECT
                product AS value,
                COUNT(product) AS count

            FROM
                lakey.shopping

            GROUP BY product
            ORDER BY count DESC
            LIMIT 123
            ''')

    #
    # GET_DISTRIBUTION_NUMERICAL
    #
    @override_settings(
        CATALOGUE_ITEMS_DISTRIBUTION_VALUE_BINS_COUNT=5)
    def test_get_distribution_numerical(self):

        execute_to_df = self.mocker.patch.object(
            AthenaExecutor, 'execute_to_df')
        execute_to_df.side_effect = [
            Mock(to_dict=Mock(return_value={'min_': [123], 'max_': [678]})),
            Mock(to_dict=Mock(return_value=[
                {'value': 0, 'count': 12},
                {'value': 1, 'count': 45},
                {'value': 2, 'count': 34},
                {'value': 3, 'count': 9},
                {'value': 4, 'count': 11},
            ])),
        ]

        assert self.executor.get_distribution_numerical(
            'quantity',
            self.ci
        ) == [
            {'value': 123, 'count': 12},
            {'value': 234, 'count': 45},
            {'value': 345, 'count': 34},
            {'value': 456, 'count': 9},
            {'value': 567, 'count': 11},
        ]
        assert execute_to_df.call_count == 2
        database, query = execute_to_df.call_args_list[0]

        assert database[0] == 'lakey'
        assert normalize_query(query['query']) == normalize_query(
            '''
                SELECT
                    MIN(quantity) AS min_,
                    MAX(quantity) AS max_
                FROM
                    lakey.shopping
            ''')

        database, query = execute_to_df.call_args_list[1]

        assert database[0] == 'lakey'
        assert normalize_query(query['query']) == normalize_query(
            '''
            SELECT
                g.bin AS value,
                COUNT(g.bin) AS count
            FROM (
                SELECT
                    quantity,
                    FLOOR(
                        5 * (quantity - 123) / (555)
                    ) AS bin
                FROM
                    lakey.shopping
                ) AS g
            GROUP BY g.bin
            ORDER BY g.bin
            ''')

    #
    # EXECUTE_TO_DF
    #
    @httpretty.activate
    def test_execute_to_df(self):

        httpretty.register_uri(
            httpretty.GET,
            'https://s3.some/results/1.csv',
            status=200,
            body='name,price\ncandy,12\nshoe,234')

        execute_query = self.mocker.patch.object(
            AthenaExecutor, 'execute_query')
        execute_query.return_value = 'https://s3.some/results/1.csv'

        assert self.executor.execute_to_df(
            'my.db',
            'SELECT * FROM everything'
        ).to_dict(orient='list') == {
            'name': ['candy', 'shoe'],
            'price': [12, 234],
        }

        assert execute_query.call_args_list == [
            call('my.db', 'SELECT * FROM everything'),
        ]

    #
    # EXECUTE_QUERY
    #
    @override_settings(
        AWS_LAKEY_RESULTS_LOCATION='s3://results/',
        AWS_S3_BUCKET='lakey',
        AWS_LAKEY_REGION='poland')
    def test_execute_query(self):

        athena = self.mocker.patch('downloader.executors.athena.athena')
        s3 = self.mocker.patch('downloader.executors.athena.s3')

        athena.start_query_execution.return_value = {
            'QueryExecutionId': 'some.exec.id',
        }

        assert self.executor.execute_query(
            'my.db.0',
            'SELECT * FROM this'
        ) == 'https://s3.poland.amazonaws.com/lakey/results/some.exec.id.csv'

        assert athena.start_query_execution.call_args_list == [
            call(
                QueryExecutionContext={'Database': 'my.db.0'},
                QueryString='SELECT * FROM this',
                ResultConfiguration={'OutputLocation': 's3://results/'}),
        ]
        assert s3.put_object.call_args_list == [
            call(
                ACL='public-read',
                Bucket='lakey',
                Key='/results/some.exec.id.csv'),
        ]
