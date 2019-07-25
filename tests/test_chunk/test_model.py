
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytest

from chunk.models import Chunk
from tests.factory import EntityFactory


ef = EntityFactory()


class ChunkTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def ci(self, overrides=None):

        if overrides is None:
            overrides = [{}, {}]

        return ef.catalogue_item(spec=[
            {
                'name': 'A',
                'type': 'STRING',
                'is_nullable': True,
                'is_enum': True,
                'size': None,
                'distribution': None,
                **overrides[0],
            },
            {
                'name': 'B',
                'type': 'INTEGER',
                'is_nullable': False,
                'is_enum': False,
                'size': None,
                'distribution': None,
                **overrides[1],
            },
        ])

    def test_simple_creation(self):

        ci = self.ci()

        c = Chunk.objects.create(
            catalogue_item=ci,
            borders=[
                {
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

        assert c.catalogue_item == ci
        assert c.borders == [
            {
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
            },
        ]

    def test_borders_validation__expect_array(self):

        ci = self.ci([{}, {}])

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders='whatever'
                )

        assert e.value.message_dict == {
            'borders': [
                "JSON did not validate. PATH: '.' REASON: 'whatever' is not of "
            "type 'array'"],
            }

        # FIXME: check that when borders is not a list!!!!! what happens

    def test_borders_should_match_columns_in_catalogue_item(self):

        ci = self.ci([{'name': 'C'}, {}])

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
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

        assert e.value.message_dict == {
            '__all__': ['borders columns do not match catalogue item']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ['borders columns do not match catalogue item']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'C',
                        'minimum': 10,
                        'maximum': 15,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ['unknown column detected']
        }

    def test_borders_validation__column_is_correct_type(self):

        #ci = self.ci([{'name': True,}, {}])
        #not working becouse of catalog item create error
        #??? ask

        ci = self.ci()

        with pytest.raises(ValidationError) as e:

            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
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
            '__all__': ['borders columns do not match catalogue item'],
            'borders': ["JSON did not validate. PATH: '0.column' REASON: True is not of "
                    "type 'string'"]
        }

    def test_borders_validation__minimum_not_null(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': '',
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ['minimum can not by empty']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
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

        #??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            'borders': ["JSON did not validate. PATH: '0.minimum' REASON: None is not "
                'valid under any of the given schemas']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': None,
                        'maximum': 25,
                    },
                ])

        #??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            'borders': ["JSON did not validate. PATH: '1.minimum' REASON: None is not "
                'valid under any of the given schemas']
        }

    def test_borders_validation__minimum_is_correct_type(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
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

        assert e.value.message_dict == {
            'borders': [
                "JSON did not validate. PATH: '0.minimum' "
                "REASON: True is not valid under any of the "
                "given schemas",
            ],
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': True,
                        'maximum': 25,
                    },
                ])

        assert e.value.message_dict == {
            'borders': [
                "JSON did not validate. PATH: '1.minimum' "
                "REASON: True is not valid under any of the "
                "given schemas",
            ],
        }

    def test_borders_validation__minimum_from_catalogue_item(self):
        pass

    def test_borders_validation__maximum_not_null(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': '',
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ['maximum can not by empty']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
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

        #??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            'borders': ["JSON did not validate. PATH: '0.maximum' REASON: None is not "
                'valid under any of the given schemas']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': None,
                    },
                ])

        #??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            'borders': ["JSON did not validate. PATH: '1.maximum' REASON: None is not "
                'valid under any of the given schemas']
        }

    def test_borders_validation__maximum_is_correct_type(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
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

        assert e.value.message_dict == {
            '__all__': ['maximum has to be greater than minimum'],
            'borders': [
                "JSON did not validate. PATH: '0.maximum' "
                "REASON: True is not valid under any of the "
                "given schemas",
            ],
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': True,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ['maximum has to be greater than minimum'],
            'borders': [
                "JSON did not validate. PATH: '1.maximum' "
                "REASON: True is not valid under any of the "
                "given schemas",
            ],
        }

    def test_borders_validation__maximum_from_catalogue_item(self):
        pass

    def test_borders_validation__maximum_is_greater_than_minimum(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
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

        assert e.value.message_dict == {
            '__all__': ["maximum has to be greater than minimum"],
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': 25,
                        'maximum': 25,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ["maximum has to be greater than minimum"],
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            Chunk.objects.create(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': 25,
                        'maximum': 20,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ["maximum has to be greater than minimum"],
        }
