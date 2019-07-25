
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytest

from catalogue.models import CatalogueItem
from chunk.models import Chunk
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemCreateChunksTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

    def ci(self, spec_overrides=None, sample_overrides=None):
        if spec_overrides is None:
            spec_overrides = [{}, {}]

        if sample_overrides is None:
            sample_overrides = [
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
            ]

        return ef.catalogue_item(
            spec=[
                {
                    'name': 'A',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                    **spec_overrides[0],
                },
                {
                    'name': 'B',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                    **spec_overrides[1],
                },
            ],
            sample=sample_overrides,
        )

    def test_simple_create__integer_column_values(self):
        spec = [
           {
               'type': 'INTEGER',
           },
           {
               'type': 'INTEGER',
           },
        ]

        sample = [
            {'A': 10, 'B': 12},
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
        ]

        ci = self.ci(spec_overrides=spec, sample_overrides=sample)
        ci.create_chunks(3)

    def test_simple_create__float_column_values(self):
        spec = [
           {
               'type': 'FLOAT',
           },
           {
               'type': 'FLOAT',
           },
        ]
        sample = [
            {'A': 10.2, 'B': 12.2},
            {'A': 11.2, 'B': 15.2},
            {'A': 30.2, 'B': 22.2},
            {'A': 41.2, 'B': 15.2},
            {'A': 50.2, 'B': 32.2},
            {'A': 61.2, 'B': 15.2},
            {'A': 70.2, 'B': 22.2},
            {'A': 81.2, 'B': 55.2},
            {'A': 20.2, 'B': 32.2},
            {'A': 31.2, 'B': 25.2},
            {'A': 31.2, 'B': 25.2},
            {'A': 31.2, 'B': 25.2},
        ]

        ci = self.ci(spec_overrides=spec, sample_overrides=sample)
        ci.create_chunks(3)

    def test_simple_create__string_column_values(self):
        spec = [
            {
                'type': 'STRING',
            },
            {
                'type': 'STRING',
            },
        ]
        sample = [
            {'A': 'KOgdfT', 'B': '234234'},
            {'A': 'KOfgdT', 'B': 'Kgdfg'},
            {'A': 'KO4ggT', 'B': 'KdfgOT'},
            {'A': 'KfdgOT', 'B': 'KfgOT'},
            {'A': 'dfgKOT', 'B': 'K23OT'},
            {'A': 'KOdfgT', 'B': 'KOT'},
            {'A': 'KOTfgg', 'B': 'KOgfgdfgT'},
            {'A': 'KfdgOT', 'B': 'KOdddgT'},
            {'A': 'KOdfgT', 'B': 'KthrOT'},
            {'A': 'KOdfgT', 'B': 'KrthOT'},
            {'A': 'KfgdOT', 'B': 'K3OT'},
            {'A': 'KOTdff', 'B': 'KOdfgT'},
        ]

        ci = self.ci(spec_overrides=spec, sample_overrides=sample)
        ci.create_chunks(3)

    def test_simple_create__boolean_column_values(self):
        spec = [
            {
                'type': 'BOOLEAN',
            },
            {
                'type': 'BOOLEAN',
            },
        ]
        sample = [
            {'A': True, 'B': False},
            {'A': False, 'B': True},
            {'A': True, 'B': False},
            {'A': False, 'B': False},
            {'A': True, 'B': False},
            {'A': False, 'B': False},
            {'A': False, 'B': False},
            {'A': True, 'B': True},
            {'A': False, 'B': False},
            {'A': False, 'B': True},
            {'A': True, 'B': False},
            {'A': False, 'B': False},
        ]

        ci = self.ci(spec_overrides=spec, sample_overrides=sample)
        ci.create_chunks(3)

    def test_simple_create__datetime_column_values(self):
        pass

    def test_simple_create__mix_column_values(self):
        pass

    def test_correct_quantity_chunks(self):
        pass
