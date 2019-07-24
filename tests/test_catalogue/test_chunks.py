
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytest

from catalogue.models import CatalogueItem
from downloader.executors.athena import AthenaExecutor
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

    def test_simple_create(self):

        a = ef.account()
        spec = [
            {
                'name': 'A',
                'type': 'INTEGER',
                'size': 190234,
                'is_nullable': False,
                'is_enum': False,
                'distribution': None,
            },
            {
                'name': 'B',
                'type': 'INTEGER',
                'size': 123132,
                'is_nullable': False,
                'is_enum': False,
                'distribution': [
                    {'value': 18, 'count': 9},
                    {'value': 19, 'count': 45},
                    {'value': 21, 'count': 10},
                    {'value': 22, 'count': 190},
                ],
            },
        ]

        ci = CatalogueItem.objects.create(
            maintained_by=a,
            name='weather_temperatures',
            sample=[
                {'A': 10, 'B': 22},
                {'A': 11, 'B': 15},
                {'A': 30, 'B': 22},
                {'A': 41, 'B': 15},
                {'A': 50, 'B': 32},
                {'A': 61, 'B': 15},
                {'A': 70, 'B': 22},
                {'A': 81, 'B': 55},
                {'A': 20, 'B': 32},
                {'A': 31, 'B': 25},
                {'A': 31, 'B': 25},
                {'A': 31, 'B': 25},
            ],
            spec=spec,
            executor_type='DATABRICKS')

        print(ci.create_chunks())



