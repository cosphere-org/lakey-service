
from django.test import TestCase
from django.core.exceptions import ValidationError
import pytest

from catalogue.models import CatalogueItem
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_simple_create(self):

        a = ef.account()
        spec = [
            {
                'name': 'location',
                'type': 'STRING',
                'size': 190234,
                'is_nullable': False,
                'distribution': None,
            },
            {
                'name': 'value',
                'type': 'FLOAT',
                'size': None,
                'is_nullable': True,
                'distribution': [
                    {'value': 18.0, 'count': 9},
                    {'value': 19.1, 'count': 45},
                    {'value': 21.2, 'count': 10},
                    {'value': None, 'count': 190},
                ],
            },
        ]

        ci = CatalogueItem.objects.create(
            maintained_by=a,
            name='weather_temperatures',
            sample=[
                {'location': 'Warsaw', 'value': 19.2},
                {'location': 'Wroclaw', 'value': 17.9},
            ],
            spec=spec,
            executor_type='DATABRICKS')

        assert ci.created_datetime is not None
        assert ci.updated_datetime is not None
        assert ci.created_by is None
        assert ci.updated_by is None
        assert ci.maintained_by == a
        assert ci.name == 'weather_temperatures'
        assert ci.sample == [
            {'location': 'Warsaw', 'value': 19.2},
            {'location': 'Wroclaw', 'value': 17.9},
        ]
        assert ci.spec == spec

    def test_invalid__name_should_be_unique(self):

        ef.catalogue_item(name='feature')

        with pytest.raises(ValidationError) as e:
            ef.catalogue_item(name='feature')

        assert e.value.message_dict == {
            'name': ['Catalogue item with this Name already exists.'],
        }

    def test_invalid__broken_spec_schema__missing_fields(self):

        a = ef.account()
        spec = [
            {
                'type': 'STRING',
                'size': 190234,
                'is_nullable': False,
                'distribution': None,
            },
        ]

        with pytest.raises(ValidationError) as e:
            CatalogueItem.objects.create(
                maintained_by=a,
                name='weather_temperatures',
                sample=[],
                spec=spec,
                executor_type='DATABRICKS')

        assert e.value.message_dict == {
            'spec': [
                "JSON did not validate. PATH: '0' REASON: 'name' is a "
                "required property",
            ],
        }

    def test_invalid__broken_spec_schema__wrong_type(self):

        a = ef.account()
        spec = [
            {
                'name': 'price',
                'type': 'STRING',
                'size': '190234',
                'is_nullable': False,
                'distribution': None,
            },
        ]

        with pytest.raises(ValidationError) as e:
            CatalogueItem.objects.create(
                maintained_by=a,
                name='weather_temperatures',
                sample=[],
                spec=spec,
                executor_type='DATABRICKS')

        assert e.value.message_dict == {
            'spec': [
                "JSON did not validate. PATH: '0.size' REASON: '190234' "
                "is not valid under any of the given schemas",
            ],
        }

    def test_invalid__broken_spec_distribution_types(self):

        a = ef.account()
        spec = [
            {
                'name': 'value',
                'type': 'FLOAT',
                'size': None,
                'is_nullable': True,
                'distribution': [
                    {'value': 18.0, 'count': 9},
                    {'value': '19', 'count': 45},
                    {'value': 21.2, 'count': 10},
                ],
            },
        ]

        with pytest.raises(ValidationError) as e:
            CatalogueItem.objects.create(
                maintained_by=a,
                name='weather_temperatures',
                sample=[],
                spec=spec,
                executor_type='DATABRICKS')

        assert e.value.message_dict == {
            'spec': [
                "column type and distribution value type mismatch detected "
                "for column 'value'",
            ],
        }

    def test_invalid__broken_spec_distribution__values_not_unique(self):

        a = ef.account()
        spec = [
            {
                'name': 'value',
                'type': 'FLOAT',
                'size': None,
                'is_nullable': True,
                'distribution': [
                    {'value': 19.0, 'count': 9},
                    {'value': 19.0, 'count': 45},
                    {'value': 21.2, 'count': 10},
                ],
            },
        ]

        with pytest.raises(ValidationError) as e:
            CatalogueItem.objects.create(
                maintained_by=a,
                name='weather_temperatures',
                sample=[],
                spec=spec,
                executor_type='DATABRICKS')

        assert e.value.message_dict == {
            'spec': [
                "not unique distribution values for column 'value' detected",
            ],
        }

    def test_invalid__broken_spec_distribution__counts_not_integers(self):

        a = ef.account()
        spec = [
            {
                'name': 'value',
                'type': 'FLOAT',
                'size': None,
                'is_nullable': True,
                'distribution': [
                    {'value': 19.0, 'count': 45.9},
                    {'value': 21.2, 'count': 10},
                ],
            },
        ]

        with pytest.raises(ValidationError) as e:
            CatalogueItem.objects.create(
                maintained_by=a,
                name='weather_temperatures',
                sample=[],
                spec=spec,
                executor_type='DATABRICKS')

        assert e.value.message_dict == {
            'spec': [
                "not integers distribution counts for column 'value' detected",
            ],
        }

    def test_invalid__broken_sample_not_same_names(self):

        a = ef.account()
        spec = [
            {
                'name': 'name',
                'type': 'STRING',
                'size': None,
                'is_nullable': True,
                'distribution': None,
            },
            {
                'name': 'price',
                'type': 'FLOAT',
                'size': None,
                'is_nullable': True,
                'distribution': None,
            },
        ]

        with pytest.raises(ValidationError) as e:
            CatalogueItem.objects.create(
                maintained_by=a,
                name='weather_temperatures',
                sample=[
                    {'name': 'apple'},
                    {'name': 'juice', 'price': 16},
                ],
                spec=spec,
                executor_type='DATABRICKS')

        assert e.value.message_dict == {
            '__all__': [
                'Sample column names and spec names are not identical',
            ],
        }

    def test_invalid__broken_sample_broken_types(self):

        a = ef.account()
        spec = [
            {
                'name': 'name',
                'type': 'STRING',
                'size': None,
                'is_nullable': True,
                'distribution': None,
            },
            {
                'name': 'price',
                'type': 'FLOAT',
                'size': None,
                'is_nullable': True,
                'distribution': None,
            },
        ]

        with pytest.raises(ValidationError) as e:
            CatalogueItem.objects.create(
                maintained_by=a,
                name='weather_temperatures',
                sample=[
                    {'name': 'apple', 'price': 'free'},
                    {'name': 'juice', 'price': 16},
                ],
                spec=spec,
                executor_type='DATABRICKS')

        assert e.value.message_dict == {
            '__all__': [
                "column type and sample value type mismatch detected for row "
                "number 0 column 'price'",
            ],
        }
