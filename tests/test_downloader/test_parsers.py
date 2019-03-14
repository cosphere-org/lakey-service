
from django.test import TestCase

from downloader.parsers import (
    DownloadRequestParser,
    DownloadRequestRenderParser,
)
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestRenderParserTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_parse(self):

        parser = DownloadRequestRenderParser(data={
            'catalogue_item_id': 839,
        })

        assert parser.is_valid() is True
        assert parser.errors == {}
        assert parser.data == {
            'catalogue_item_id': 839,
        }

    def test_parse__invalid(self):

        parser = DownloadRequestRenderParser(data={
            'catalogue_item_id': 'whatever',
        })

        assert parser.is_valid() is False
        assert parser.errors == {
            'catalogue_item_id': ['A valid integer is required.'],
        }


class DownloadRequestParserTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_parse(self):

        parser = DownloadRequestParser(data={
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
            'catalogue_item_id': 1902,
        })
        assert parser.is_valid() is True
        assert parser.errors == {}
        assert parser.data == {
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
            'catalogue_item_id': 1902,
        }

    def test_parse__invalid(self):

        parser = DownloadRequestParser(data={
            'spec': {
                'columns': ['product'],
                'filters': [
                    {
                        'name': 'price',
                        'operator': '>>',
                        'value': 120,
                    },
                ],
                'randomize_ratio': 0.9,
            },
            'catalogue_item_id': 1902,
        })
        assert parser.is_valid() is False
        assert parser.errors == {
            'spec': [
                "JSON did not validate. PATH: 'filters.0.operator' REASON: "
                "'>>' is not one of ['>', '>=', '<', '<=', '=', '!=']",
            ],
        }
