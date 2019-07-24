
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
            ])


    def test_simple_creation(self):

        c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert c.catalogue_item == self.ci
        assert c.borders == [{
            'column': 'A',
            'minimum': 10,
            'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },]


    def test_borders_empty(self):

        with pytest.raises(ValidationError) as e:
            c = Chunk.objects.create(
                catalogue_item=self.ci,
                borders=[])
        assert e.value.message_dict['__all__'][0] == "chunk - borders must be created"


    def test_different_number_of_elements(self):

        with pytest.raises(ValidationError) as e:
            ci = ef.catalogue_item(
                spec=[
                    {
                        'name': "A",
                        'type': 'STRING',
                        'is_nullable': True,
                        'is_enum': True,
                        'size': None,
                        'distribution': None,
                    },
                ])

            c = Chunk.objects.create(
            catalogue_item=ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict['__all__'][0] == "borders have to have same number of entries as catalogue_item.spec"
        #######how to split this line#############

    def test_borders_validation__all_columns_must_be_present(self):
        pass    

    def test_borders_validation__expect_array(self):

        c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert type(c.borders).__name__ == "list"


    def test_borders_validation__column_not_null(self):

        with pytest.raises(ValidationError) as e:
            ci = ef.catalogue_item(
                    spec=[
                        {
                            'name': '',
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
                    ])

            ##########empty string passed by schema validation##########

            c = Chunk.objects.create(
            catalogue_item=ci,
            borders=[{
                'column': '',
                'minimum': 10,
                'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict['__all__'][0] == "column can not by empty"


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
                    {
                        'name': 'B',
                        'type': 'INTEGER',
                        'is_nullable': False,
                        'is_enum': False,
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
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

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
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict == {'__all__': ['unknown column detected']}


    def test_borders_validation__minimum_not_null(self):

        with pytest.raises(ValidationError) as e:
            c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': None,
                'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict['__all__'][0] == "minimum can not by empty"

        ########shoud i test second case??##############

    def test_borders_validation__minimum_is_correct_type(self):

        with pytest.raises(ValidationError) as e:
            c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': True,
                'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict['borders'][0] == "JSON did not validate. PATH: '0.minimum' REASON: True is not valid under any of the given schemas"
        ########how to slice this line?? ##########

    def test_borders_validation__minimum_from_catalogue_item(self):
        pass

    def test_borders_validation__maximum_not_null(self):
        
        with pytest.raises(ValidationError) as e:
            c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': None,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict['__all__'][0] == "minimum can not by empty"


    def test_borders_validation__maximum_is_correct_type(self):
       
        with pytest.raises(ValidationError) as e:
            c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': True,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict['borders'][0] == "JSON did not validate. PATH: '0.maximum' REASON: True is not valid under any of the given schemas"

    def test_borders_validation__maximum_from_catalogue_item(self):
        pass

    def test_borders_validation__maximum_is_greater_than_minimum(self):
        
        with pytest.raises(ValidationError) as e:
            c = Chunk.objects.create(
            catalogue_item=self.ci,
            borders=[{
                'column': 'A',
                'minimum': 10,
                'maximum': 10,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
            ])

        assert e.value.message_dict['__all__'][0] == "maximum has to be greater than minimum"
