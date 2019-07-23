
from django.test import TestCase
from django.core.exceptions import ValidationError

import pytest

from chunk.models import Chunk
from tests.factory import EntityFactory


ef = EntityFactory()


class ChunkTestCase(TestCase):

    def setUp(self):
        ef.clear()

        self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'A',
                    'type': 'STRING',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'B',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'C',
                    'type': 'BOOLEAN',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                }
            ])


    def test_simple_creation(self):

        c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
            }])

        b = [{
            'column': 'A',
            'minimum': 10,
            'maximum': 15,
            }]
        assert c.catalogue_item == self.ci
#########!!!!!!!!!!!!!!!!!!!!!!!!

    def test_borders_validation__expect_array(self):

        c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
            }])

        assert type(c.borders).__name__ == "list"


    def test_borders_validation__column_not_null(self):

        c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': '',
                'minimum': 10,
                'maximum': 15,
            }])

        assert c.borders[0]['column'] is not '' or None


    def test_borders_validation__column_is_correct_type(self):

        with pytest.raises(ValidationError) as e:
            ci = ef.catalogue_item(
                spec=[
                    {
                        'name': True,
                        'type': 'STRING',
                        'is_nullable': True,
                        'is_enum': True,
                        'size': None,
                        'distribution': None,
                    },
                ])

            ####ask if it make sense????????????#######
            ###### ask about different types np. int####

            c = Chunk.objects.create(
                catalogue_item=ci,
                borders=[{
                    'column': True,
                    'minimum': 10,
                    'maximum': 15,
                }])

        assert e.value.message_dict == {
            'spec': [
                "JSON did not validate. PATH: '0.name'"
                " REASON: True is not of type 'string'"
            ],
        }

    def test_borders_validation__column_from_catalogue_item(self):

        with pytest.raises(ValidationError) as e:
            c = Chunk.objects.create(
                catalogue_item=self.ci,
                borders=[{
                    'column': 'whatever',
                    'minimum': 10,
                    'maximum': 15,
                    }])

        assert e.value.message_dict == {'__all__': ['unknown column detected']}

    def test_borders_validation__minimum_not_null(self):

        c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': '',
                'minimum': 10,
                'maximum': 15,
                }])

        assert c.borders[0]['minimum'] is not '' or None

    def test_borders_validation__minimum_is_correct_type(self):
        pass

    def test_borders_validation__minimum_from_catalogue_item(self):
        pass

    def test_borders_validation__maximum_not_null(self):
        pass

    def test_borders_validation__maximum_from_catalogue_item(self):
        pass

    def test_borders_validation__maximum_is_correct_type(self):
        pass

    def test_borders_validation__maximum_is_greater_than_minimum(self):
        pass

    def test_borders_validation__all_columns_must_be_present(self):
        pass
