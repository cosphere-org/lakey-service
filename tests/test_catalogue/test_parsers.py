
from django.test import TestCase

from catalogue.parsers import CatalogueItemCreateParser
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemCreateParserTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_parse(self):

        parser = CatalogueItemCreateParser(data={
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
            'maintained_by_id': 1289,
            'executor_type': 'DATABRICKS',
        })
        assert parser.is_valid() is True
        assert parser.errors == {}
        assert parser.data == {
            'executor_type': 'DATABRICKS',
            'maintained_by_id': 1289,
            'name': 'iot_events',
            'sample': [],
            'spec': [
                {
                    'distribution': None,
                    'is_nullable': False,
                    'is_enum': False,
                    'name': 'value',
                    'size': 19203,
                    'type': 'FLOAT',
                },
            ],
        }

    def test_parse__invalid(self):

        parser = CatalogueItemCreateParser(data={
            'name': 'iot_events',
            'sample': [],
            'spec': [
                {
                    'name': 'value',
                    'type': 'FLOAT',
                    'size': '19203',
                    'is_nullable': False,
                    'is_enum': False,
                    'distribution': None,
                },
            ],
            'maintained_by_id': 1289,
            'executor_type': 'DATABRICKS',
        })
        assert parser.is_valid() is False
        assert parser.errors == {
            'spec': [
                "JSON did not validate. PATH: '0.size' REASON: '19203' "
                "is not valid under any of the given schemas",
            ],
        }

    def test_parse__name_already_exists(self):

        ef.catalogue_item(name='iot_events')

        parser = CatalogueItemCreateParser(data={
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
            'maintained_by_id': 1289,
            'executor_type': 'DATABRICKS',
        })
        assert parser.is_valid() is False
        assert parser.errors == {
            'name': ['catalogue item with this name already exists.'],
        }
