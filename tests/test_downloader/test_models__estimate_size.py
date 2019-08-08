
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
                    'size': 120,  # sum(distribution.count) * type.size
                    'is_nullable': False,
                    'is_enum': False,
                    'distribution': [
                        {'value_min': 0, 'value_max': 10, 'count': 20},
                        {'value_min': 11, 'value_max': 20, 'count': 20},
                    ],
                },
                {
                    'name': 'B',
                    'type': 'INTEGER',
                    'size': 120,  # sum(distribution.count) * type.size
                    'is_nullable': False,
                    'is_enum': False,
                    'distribution': [
                        {'value_min': 0, 'value_max': 10, 'count': 20},
                        {'value_min': 11, 'value_max': 20, 'count': 20},
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
                            {'value_min': 18, 'value_max': 20, 'count': 10},
                            {'value_min': 19, 'value_max': 24, 'count': 10},
                        ],
                    },
                    {
                        'column': 'B',
                        'minimum': 0,
                        'maximum': 10,
                        'distribution': [
                            {'value_min': 18, 'value_max': 20, 'count': 10},
                            {'value_min': 19, 'value_max': 24, 'count': 10},
                        ],
                    },
                ],
                [
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 20,
                        'distribution': [
                            {'value_min': 18, 'value_max': 20.0, 'count': 10},
                            {'value_min': 19, 'value_max': 24, 'count': 10},
                        ],
                    },
                    {
                        'column': 'B',
                        'minimum': 10,
                        'maximum': 20,
                        'distribution': [
                            {'value_min': 18, 'value_max': 20, 'count': 10},
                            {'value_min': 19, 'value_max': 24, 'count': 10},
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

        es = DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert es['size'] == 0

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

        es = DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert es['size'] == 120

    def test_estimate_size__filters_include_too_much_data(self):
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
                    'value': 20,
                },
            ],
            'randomize_ratio': 1,
        }

        with pytest.raises(TooMuchDataRequestDetected) as e:
            DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert str(e.value) == f"specify filters to a smaller data area"

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

        es = DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert es['size'] == 120

    def test_estimate_size__filters_without_offset(self):
        spec = {
            'columns': ['A'],
            'filters': [
                {
                    'name': 'A',
                    'operator': '>=',
                    'value': 10,
                },
                {
                    'name': 'A',
                    'operator': '<=',
                    'value': 20,
                },
            ],
            'randomize_ratio': 1,
        }

        es = DownloadRequest.objects.estimate_size(spec, self.ci.id)

        assert es['size'] == 120

    def test_estimate_size__chunks_not_exist(self):
        ef.clear()

        with pytest.raises(NoChunksDetected) as e:
            DownloadRequest.objects.estimate_size({}, self.ci.id)

        assert str(e.value) == f"chunks must exist for " \
                               f"indicated catalogue item"

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
