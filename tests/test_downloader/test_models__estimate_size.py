
from django.test import TestCase
from django.core.exceptions import ValidationError

import pytest

from downloader.models import DownloadRequest
from tests.factory import EntityFactory
from downloader.models import MutuallyExclusiveFiltersDetected, NoFiltersDetected


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

        self.chs = ef.chunk_bulk(
            chunks_borders=[
                [
                    {
                        'column': 'A',
                        'minimum': 0,
                        'maximum': 10,
                    },
                ],
                [
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 20,
                    },
                ],
            ],
            catalogue_item=self.ci,
            count=1,
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

        es = DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert es == 8

    # def test_estimate_size__filter_column_is_empty(self): pass
    # def test_estimate_size__filter_include_all(self): pass
    # def test_estimate_size__filter_with_offset(self): pass
    # def test_estimate_size__filter_without_offset(self): pass
    # def test_estimate_size__chunks_not_exist(self): pass

    def test_simplify_spec__filters_is_empty(self):
        spec = {
            'columns': ['A'],
            'filters': [],
            'randomize_ratio': 1,
        }

        with pytest.raises(NoFiltersDetected) as e:
            DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert str(e.value) == f"spec must have at least one filter '{spec}'"

    def test_simplify_spec__many_equal_or_less_and_less_operator(self):
        spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '<',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '<=',
                    'value': 20,
                },
            ]
        }

        expected_spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '<',
                    'value': 0,
                },
            ]
        }

        pull_spec = DownloadRequest.objects.simplify_spec(spec)
        assert pull_spec == expected_spec

    def test_simplify_spec__many_equal_or_greater_and_greater_operator(self):
        spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '>',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '>=',
                    'value': 20,
                },
            ]
        }

        expected_spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '>',
                    'value': 20,
                },
            ]
        }

        pull_spec = DownloadRequest.objects.simplify_spec(spec)
        assert pull_spec == expected_spec

    def test_simplify_spec__many_equal_operator(self):
        spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '=',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '=',
                    'value': 20,
                },
            ]
        }

        with pytest.raises(MutuallyExclusiveFiltersDetected) as e:
            DownloadRequest.objects.simplify_spec(spec)

        assert str(e.value) == f"spec filters can not have multiple equal operators '{spec}'"

    def test_simplify_spec__many_less_operator(self):
        spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '<',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '<',
                    'value': 20,
                },
            ]
        }

        expected_spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '<',
                    'value': 0,
                },
            ]
        }

        pull_spec = DownloadRequest.objects.simplify_spec(spec)
        assert pull_spec == expected_spec

    def test_simplify_spec__many_same_operator(self):
        spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '>',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '>',
                    'value': 20,
                },
            ]
        }

        expected_spec = {
            'filters': [
                {
                    'name': 'A',
                    'operator': '>',
                    'value': 20,
                },
            ]
        }

        pull_spec = DownloadRequest.objects.simplify_spec(spec)
        assert pull_spec == expected_spec
