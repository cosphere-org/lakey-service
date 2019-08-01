
from django.test import TestCase
from django.core.exceptions import ValidationError

import pytest

from downloader.models import DownloadRequest
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestEstimateSizeTestCase(TestCase):

    def setUp(self):
        ef.clear()

        self.ci = ef.catalogue_item()

    def test_estimate_size__filter_with_open_range(self):


        d = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['A'],
                'filters': [
                    {
                        'name': 'A',
                        'operator': '>=',
                        'value': 10,
                    },
                    {
                        'name': 'B',
                        'operator': '=',
                        'value': 22,
                    },

                ],
                'randomize_ratio': 1,
            },
            catalogue_item=self.ci)

        est = DownloadRequest.objects.estimate_size(d.spec, self.ci.pk)

        assert est

    def test_estimate_size__filter_with_closed_range(self):
        ci = ef.catalogue_item(
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

        ef.chunk_bulk([
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
        ])

        es = DownloadRequest.objects.estimate_size(spec, ci.id)

        assert es == 8


    def test_estimate_size__filter_is_empty(self):
        pass

    def test_estimate_size__filter_include_all(self):
        pass

    def test_estimate_size__filter_with_offset(self):
        pass

    def test_estimate_size__filter_without_offset(self):
        pass

    def test_estimate_size__chunks_not_exist(self):
        pass
