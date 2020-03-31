
# import re
from unittest.mock import Mock, call

from databricks_api import DatabricksAPI
from django.test import TestCase, override_settings
# import httpretty
import pytest

# from downloader.models import DownloadRequest
from downloader.executors.databricks import DatabricksExecutor
from tests.factory import EntityFactory


ef = EntityFactory()


# def normalize_query(q):
#     return re.sub(r'\s+', ' ', q).strip()


class DatabricksExecutorTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

        self.executor = DatabricksExecutor()

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
            ],
            executor_type='DATABRICKS'
        )

    #
    # EXECUTE_QUERY
    #
    @override_settings(
        DATABRICKS_HOST='https:/databricks.com',
        DATABRICKS_CLUSTER_ID='abc123',
        DATABRICKS_SCRIPT_LOCATION='dbfs://scripts'
    )
    def test_execute_query(self):

        submit_run = self.mocker.patch.object(
            self.executor.db.jobs,
            'submit_run'
        )

        get_output_file_path = self.mocker.patch.object(
            self.executor,
            'get_output_file_path'
        )

        get_output_file_path.return_value = 'dbfs://output_file.csv'

        assert self.executor.execute_query(
            'SELECT * from everywhere'
        ) == 'https:/databricks.com'

        assert submit_run.call_args_list == [
            call(
                run_name='Lakey get data',
                existing_cluster_id='abc123',
                spark_python_task={
                    'python_file': 'dbfs://scripts',
                    'parameters': [
                        'SELECT * from everywhere',
                        'dbfs://output_file.csv'
                    ]
                }
            )
        ]
