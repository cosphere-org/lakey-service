
from django.test import TestCase

from downloader.models import DownloadRequest
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestEstimateSizeTestCase(TestCase):

    def setUp(self):
        ef.clear()

        self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'A',
                    'type': 'INTEGER',
                    'size': 123,
                    'is_nullable': False,
                    'is_enum': False,
                    'distribution': None,
                },
            ],
        )

    def test_estimate_size__filter_with_open_range(self):
        spec = {
            'columns': ['A'],
            'filters': [
                {
                    'name': 'A',
                    'operator': '<',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '>',
                    'value': 20,
                },
            ],
            'randomize_ratio': 1,
        }

        ef.chunk_bulk(
            chunks_borders=[
                [
                    {
                        'column': 'A',
                        'minimum': 0,
                        'maximum': 10,
                        'distribution': None,
                    },
                ],
                [
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 20,
                        'distribution': None,
                    },
                ],
            ],
            catalogue_item=self.ci,
            count=1,
        )

        es = DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert es == 0

    def test_estimate_size__filter_with_closed_range(self):

        spec = {
            'columns': ['A'],
            'filters': [
                {
                    'name': 'A',
                    'operator': '>',
                    'value': 5,
                },
                {
                    'name': 'A',
                    'operator': '<',
                    'value': 15,
                },
            ],
            'randomize_ratio': 1,
        }

        ef.chunk_bulk(
            chunks_borders=[
                [
                    {
                        'column': 'A',
                        'minimum': 0,
                        'maximum': 10,
                        'distribution': None,
                    },
                ],
                [
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 20,
                        'distribution': None,
                    },
                ],
            ],
            catalogue_item=self.ci,
            count=1,

        )

        assert DownloadRequest.objects.estimate_size(spec, self.ci.id) == 8

    def test_estimate_size__filters_is_empty(self):

        ef.chunk_bulk(
            chunks_borders=[
                [
                    {
                        'column': 'A',
                        'minimum': 0,
                        'maximum': 10,
                        'distribution': None,
                    },
                ],
                [
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 20,
                        'distribution': None,
                    },
                ],
            ],
            catalogue_item=self.ci,

        )

    def test_estimate_size__filter_column_is_empty(self):

        ef.chunk_bulk(
            chunks_borders=[
                [
                    {
                        'column': 'A',
                        'minimum': 0,
                        'maximum': 10,
                        'distribution': None,
                    },
                ],
                [
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 20,
                        'distribution': None,
                    },
                ],
            ],
            catalogue_item=self.ci,
        )

    def test_estimate_size__filter_include_all(self):
        pass

    def test_estimate_size__filter_with_offset(self):
        pass

    def test_estimate_size__filter_without_offset(self):
        pass

    def test_estimate_size__chunks_not_exist(self):
        pass

    def test_estimate_size__filters_exclude_themselves(self):
        pass
