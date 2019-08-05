
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytest

from tests.factory import EntityFactory
from chunk.models import Chunk


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

    def c(self, overrides=None, catalogue_item=None, borders=None):

        if overrides is None:
            overrides = [{}, {}]

        return ef.chunk(
            catalogue_item=catalogue_item,
            borders=borders or [
                {
                    'column': 'A',
                    'minimum': 10,
                    'maximum': 15,
                    'distribution': None,
                    **overrides[0],
                },
                {
                    'column': 'B',
                    'minimum': 20,
                    'maximum': 25,
                    'distribution': None,
                    **overrides[1],
                },
            ],
        )

    def test_simple_creation(self):

        ci = self.ci()
        assert Chunk.objects.count() == 0
        c = self.c(catalogue_item=ci)
        assert Chunk.objects.count() == 1
        c = Chunk.objects.first()

        assert c.created_datetime is not None
        assert c.updated_datetime is not None
        assert c.catalogue_item == ci
        assert c.borders == [
            {
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
                'distribution': None,
            },
            {
                'column': 'B',
                'minimum': 20,
                'maximum': 25,
                'distribution': None,
            },
        ]
        assert c.count is not None
        assert all(border['distribution'] is None for border in c.borders)

    def test_count__correct_type(self):

        ci = self.ci()
        c = self.c(catalogue_item=ci)

        assert type(c.count).__name__ == 'int'

    def test_borders_validation__expect_array(self):

        ci = self.ci([{}, {}])

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders='whatever'
            )

        assert e.value.message_dict == {
            '__all__': ['chunk - borders must be created and type list'],
            'borders': [
                "JSON did not validate. PATH: '.' REASON: 'whatever' is "
                "not of type 'array'"],
        }

    def test_borders_should_match_columns_in_catalogue_item(self):

        ci = self.ci([{'name': 'C'}, {}])

        with pytest.raises(ValidationError) as e:
            self.c(catalogue_item=ci)

        assert e.value.message_dict == {
            '__all__': ['borders columns do not match catalogue item']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                ]
            )

        assert e.value.message_dict == {
            '__all__': ['borders columns do not match catalogue item']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'C',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ['borders columns do not match catalogue item']
        }

    def test_borders_validation__column_is_correct_type(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:

            self.c(
                overrides=[{'column': True}, {}],
                catalogue_item=ci
            )

        assert e.value.message_dict == {
            '__all__': ['borders columns do not match catalogue item'],
            'borders': [
                "JSON did not validate. PATH: '0.column' REASON: "
                "True is not of type 'string'"
            ]
        }

    def test_borders_validation__minimum_not_null(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                overrides=[{}, {'minimum': ''}],
                catalogue_item=ci,
            )

        # ??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            '__all__': ['minimum can not be empty'],
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                overrides=[{}, {'minimum': None}],
                catalogue_item=ci,
            )

        # ??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            '__all__': ['minimum can not be empty'],
            'borders': [
                "JSON did not validate. PATH: '1.minimum' REASON: None "
                "is not valid under any of the given schemas"
            ]
        }

    def test_borders_validation__minimum_is_correct_type(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': True,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'distribution': None,
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
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': True,
                        'maximum': 25,
                        'distribution': None,
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

        ci = self.ci([
            {
                'distribution': [
                    {'value_min': "temperature1.1",
                        'value_max': "temperature2.1", 'count': 9},
                    {'value_min': "temperature1.2",
                        'value_max': "temperature2.2", 'count': 21},
                    {'value_min': "temperature1.3",
                        'value_max': "temperature2.3", 'count': 49},
                ],
            },
            {
                'distribution': [
                    {'value_min': 18, 'value_max': 20, 'count': 9},
                    {'value_min': 22, 'value_max': 24, 'count': 21},
                    {'value_min': 25, 'value_max': 32, 'count': 49},
                ],
            },
        ])

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 'temperature1.1',
                        'maximum': 'temperature2.3',
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 1,
                        'maximum': 32,
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': [
                'borders minimu has to be greater than catalogue_item minimum']
        }

    def test_borders_validation__maximum_not_null(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': '',
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ['maximum can not be empty']
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': None,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'distribution': None,
                    },
                ])

        # ??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            '__all__': ['maximum can not be empty'],
            'borders': [
                "JSON did not validate. PATH: '0.maximum' REASON: "
                'None is not valid under any of the given schemas'
            ]
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': None,
                        'distribution': None,
                    },
                ])

        # ??? ask why validation function do not raise errors
        assert e.value.message_dict == {
            '__all__': ['maximum can not be empty'],
            'borders': [
                "JSON did not validate. PATH: '1.maximum' REASON: None is not "
                'valid under any of the given schemas'
            ]
        }

    def test_borders_validation__maximum_is_correct_type(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': True,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'distribution': None,
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
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': True,
                        'distribution': None,
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

        ci = self.ci([{
            'distribution': [
                {'value_min': "temperature1.1", 'value_max': "temperature2.1",
                    'count': 9},
                {'value_min': "temperature1.2", 'value_max': "temperature2.2",
                    'count': 21},
                {'value_min': "temperature1.3", 'value_max': "temperature2.3",
                    'count': 49},
            ],
        },
            {
            'distribution': [
                {'value_min': 18, 'value_max': 20, 'count': 9},
                {'value_min': 22, 'value_max': 24, 'count': 21},
                {'value_min': 25, 'value_max': 32, 'count': 49},
            ],
        },
        ])

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 'temperature1.1',
                        'maximum': 'temperature2.3',
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 18,
                        'maximum': 9983,
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': [
                'borders maximum has to be greater than'
                ' catalogue_item maximum']
        }

    def test_borders_validation__maximum_is_greater_than_minimum(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 10,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ["maximum has to be greater than minimum"],
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 25,
                        'maximum': 25,
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ["maximum has to be greater than minimum"],
        }

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'distribution': None,
                    },
                    {
                        'column': 'B',
                        'minimum': 25,
                        'maximum': 20,
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            '__all__': ["maximum has to be greater than minimum"],
        }

    def test_distribution__invalid_distribution_types(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'type': 'FLOAT',
                        'distribution': [
                            {'value_min': 18, 'value_max': 20.0,
                                'count': 9},

                            {'value_min': 19.0, 'value_max': 24.0,
                                'count': 21},

                            {'value_min': 25.0, 'value_max': 32.0,
                                'count': 49},
                        ],
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'type': 'FLOAT',
                        'distribution': None,
                    },
                ])

            assert e.value.message_dict == {
                'borders': [
                    "column type and distribution value "
                    "type mismatch detected for column 'A'"
                ]
            }

    def test_distribution__values_not_unique(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'type': 'FLOAT',
                        'distribution': [
                            {'value_min': 18.0, 'value_max': 20.0,
                                'count': 9},

                            {'value_min': 18.0, 'value_max': 24.0,
                                'count': 21},

                            {'value_min': 25.0, 'value_max': 32.0,
                                'count': 49},
                        ],
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'type': 'FLOAT',
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            'borders':
            [
                "not unique distribution values for column 'A' detected"
            ]
        }

    def test_distribution__counts_not_integers(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'type': 'FLOAT',
                        'distribution': [
                            {'value_min': 18.0, 'value_max': 20.0,
                                'count': '9'},

                            {'value_min': 19.0, 'value_max': 24.0,
                                'count': 21},

                            {'value_min': 25.0, 'value_max': 32.0,
                                'count': 49},
                        ],
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'type': 'FLOAT',
                        'distribution': None,
                    },
                ])
        # !!! fix me:
        # how do i slice this line
        assert e.value.message_dict == {
            'borders': ["JSON did not validate. PATH: '0.distribution' REASON: [{'value_min': 18.0, 'value_max': 20.0, 'count': '9'}, {'value_min': 19.0, 'value_max': 24.0, 'count': 21}, {'value_min': 25.0, 'value_max': 32.0, 'count': 49}] is not valid under any of the given schemas", "not integers distribution counts for column 'A' detected"] # noqa
        }

    def test_distribution__extremas_valid_with_chunk(self):

        ci = self.ci()

        with pytest.raises(ValidationError) as e:
            self.c(
                catalogue_item=ci,
                borders=[
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                        'type': 'FLOAT',
                        'distribution': [
                            {'value_min': 3.0, 'value_max': 20.0,
                                'count': 9},

                            {'value_min': 19.0, 'value_max': 24.0,
                                'count': 21},

                            {'value_min': 25.0, 'value_max': 32.0,
                                'count': 49},
                        ],
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                        'type': 'FLOAT',
                        'distribution': None,
                    },
                ])

        assert e.value.message_dict == {
            
        }