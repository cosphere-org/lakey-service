
from django.test import TestCase

from catalogue.parsers import CatalogueItemParser
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemParserTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_parse(self):

        parsed = CatalogueItemParser(data={
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
            'maintained_by_id': 1289,
            'executor_type': 'DATABRICKS',
        })
        assert parsed.is_valid() is True
        assert parsed.errors == {}
        assert parsed.data == {
            'executor_type': 'DATABRICKS',
            'maintained_by_id': 1289,
            'name': 'iot_events',
            'sample': [],
            'spec': [
                {
                    'distribution': None,
                    'is_nullable': False,
                    'name': 'value',
                    'size': 19203,
                    'type': 'FLOAT',
                },
            ],
        }

    def test_parse__invalid(self):

        parsed = CatalogueItemParser(data={
            'name': 'iot_events',
            'sample': [],
            'spec': [
                {
                    'name': 'value',
                    'type': 'FLOAT',
                    'size': '19203',
                    'is_nullable': False,
                    'distribution': None,
                },
            ],
            'maintained_by_id': 1289,
            'executor_type': 'DATABRICKS',
        })
        assert parsed.is_valid() is False
        assert parsed.errors == {
            'spec': [
                "JSON did not validate. PATH: '0.size' REASON: '19203' "
                "is not valid under any of the given schemas",
            ],
        }
