
from django.test import TestCase
import pytest

from downloader.models import DownloadRequest
from tests.factory import EntityFactory
from downloader.models import (
    MutuallyExclusiveFiltersDetected,
    NoFiltersDetected,
    NoChunksDetected,
    TooMuchDataRequestDetected,
)


ef = EntityFactory()


class DownloadRequestEstimateSizeTestCase(TestCase):

    def setUp(self):
        ef.clear()

        self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'A',
                    'type': 'INTEGER',
                    'size': 480,  # sum(distribution.count) * type.size(int, 4 bit), (60 + 60) * 4
                    'is_nullable': False,
                    'is_enum': False,
                    'distribution': [
                        {'value_min': 0, 'value_max': 10, 'count': 60},
                        {'value_min': 11, 'value_max': 20, 'count': 60},
                    ],
                },
            ]
        )

        self.chs = ef.chunk_bulk(
            chunks_borders=[
                [
                    {
                        'column': 'A',
                        'minimum': 0,
                        'maximum': 10,
                        'distribution': [
                            {'value_min': 0, 'value_max': 5, 'count': 30},
                            {'value_min': 6, 'value_max': 10, 'count': 30},
                        ],
                    },
                ],
                [
                    {
                        'column': 'A',
                        'minimum': 11,
                        'maximum': 20,
                        'distribution': [
                            {'value_min': 11, 'value_max': 15, 'count': 30},
                            {'value_min': 16, 'value_max': 20, 'count': 30},
                        ],
                    },
                ],
            ],
            catalogue_item=self.ci,
            count=1,
        )

    def test_estimate_size__filters_with_open_range(self):
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

        es_size, es_chunks = \
            DownloadRequest.objects.estimate_size_and_chunks(spec, self.ci.id)

        assert es_size == 0

    def test_estimate_size__filters_with_closed_range(self):

        spec = {
            'columns': ['A'],
            'filters': [
                {
                    'name': 'A',
                    'operator': '>=',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '<=',
                    'value': 10,
                },
            ],
            'randomize_ratio': 1,
        }

        es_size, es_chunks = \
            DownloadRequest.objects.estimate_size_and_chunks(spec, self.ci.id)

        assert es_size == (30 + 30) * 4

    def test_estimate_size__filters_with_offset(self):
        spec = {
            'columns': ['A'],
            'filters': [
                {
                    'name': 'A',
                    'operator': '>=',
                    'value': 0,
                },
                {
                    'name': 'A',
                    'operator': '<=',
                    'value': 15,
                },
            ],
            'randomize_ratio': 1,
        }

        es_size, es_chunks = \
            DownloadRequest.objects.estimate_size_and_chunks(spec, self.ci.id)

        assert es_size == ((30 + 30) + (30 + 30)) * 4

    def test_estimate_size__filters_without_offset(self):
        spec = {
            'columns': ['A'],
            'filters': [
                {
                    'name': 'A',
                    'operator': '>=',
                    'value': 11,
                },
                {
                    'name': 'A',
                    'operator': '<=',
                    'value': 20,
                },
            ],
            'randomize_ratio': 1,
        }

        es_size, es_chunks = \
            DownloadRequest.objects.estimate_size_and_chunks(spec, self.ci.id)

        assert es_size == (30 + 30) * 4

    def test_estimate_size__chunks_not_exist(self):
        ef.clear()

        with pytest.raises(NoChunksDetected) as e:
            DownloadRequest.objects.estimate_size_and_chunks({}, self.ci.id)

        assert str(e.value) == f"chunks must exist for " \
                               f"indicated catalogue item"

    def test_simplify_spec__filters_is_empty(self):
        spec = {
            'columns': ['A'],
            'filters': [],
            'randomize_ratio': 1,
        }

        with pytest.raises(NoFiltersDetected) as e:
            DownloadRequest.objects.estimate_size_and_chunks(spec, self.ci.id)

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

        assert str(e.value) == (
            f"spec filters can not have multiple equal operators '{spec}'")

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
