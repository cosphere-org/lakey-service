
from django.test import TestCase
from django.core.exceptions import ValidationError

import pytest

from downloader.models import DownloadRequest
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestTestCase(TestCase):

    def setUp(self):
        ef.clear()

        self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'product',
                    'type': 'STRING',
                    'is_nullable': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'price',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'available',
                    'type': 'BOOLEAN',
                    'is_nullable': False,
                    'size': None,
                    'distribution': None,
                }
            ])

    def test_simple_create(self):

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            spec={
                'columns': ['product'],
                'filters': [
                    {
                        'name': 'price',
                        'operator': '>=',
                        'value': 78,
                    },
                ],
                'randomize_ratio': 1,
            },
            catalogue_item=self.ci)

        assert d.created_by == a
        assert d.spec == {
            'columns': ['product'],
            'filters': [
                {
                    'name': 'price',
                    'operator': '>=',
                    'value': 78,
                },
            ],
            'randomize_ratio': 1,
        }
        assert d.catalogue_item == self.ci

    def test_broken_spec__missing_fields(self):

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product'],
                    'filters': [
                        {
                            'name': 'price',
                            'value': 78,
                        },
                    ],
                    'randomize_ratio': 1,
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            'spec': [
                "JSON did not validate. PATH: 'filters.0' REASON: 'operator' "
                "is a required property",
            ],
        }

    def test_broken_spec__wrong_fields_values(self):

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product'],
                    'filters': [
                        {
                            'name': 'price',
                            'operator': '>=',
                            'value': 78,
                        },
                    ],
                    'randomize_ratio': '1',
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            'spec': [
                "JSON did not validate. PATH: 'randomize_ratio' REASON: '1' "
                "is not of type 'number'",
            ],
        }

    def test_broken_spec__not_inline_with_catalogue_spec__unknown_columns(self):  # noqa

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product', 'name'],
                    'filters': [
                        {
                            'name': 'price',
                            'operator': '>=',
                            'value': 78,
                        },
                    ],
                    'randomize_ratio': 1.2,
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': ["unknown columns in 'columns' detected: 'name'"],
        }

    def test_broken_spec__not_inline_with_catalogue_spec__unknown_filters(self):  # noqa

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product'],
                    'filters': [
                        {
                            'name': 'salary',
                            'operator': '>=',
                            'value': 78,
                        },
                    ],
                    'randomize_ratio': 1.2,
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': ["unknown columns in 'filters' detected: 'salary'"],
        }

    def test_broken_spec__not_inline_with_catalogue_spec__unknown_operator(self):  # noqa

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product'],
                    'filters': [
                        {
                            'name': 'price',
                            'operator': '>>',
                            'value': 78,
                        },
                    ],
                    'randomize_ratio': 1.2,
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': [
                "operator '>>' not allowed for column 'price' detected",
            ],
            'spec': [
                "JSON did not validate. PATH: 'filters.0.operator' REASON: "
                "'>>' is not one of ['>', '>=', '<', '<=', '=', '!=']",
            ],
        }

    def test_broken_spec__not_inline_with_catalogue_spec__not_allowed_operator(self):  # noqa

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product'],
                    'filters': [
                        {
                            'name': 'available',
                            'operator': '>=',
                            'value': True,
                        },
                    ],
                    'randomize_ratio': 1.2,
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': [
                "operator '>=' not allowed for column 'available' detected",
            ],
        }

    def test_broken_spec__not_inline_with_catalogue_spec__broken_type(self):

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product'],
                    'filters': [
                        {
                            'name': 'available',
                            'operator': '>=',
                            'value': 167,
                        },
                    ],
                    'randomize_ratio': 1.2,
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': [
                "column type and filter value type mismatch detected for "
                "column 'available'",
            ],
        }

    def test_broken_spec__randomize_ratio__not_in_allowed_range(self):

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['product'],
                    'filters': [
                        {
                            'name': 'price',
                            'operator': '>=',
                            'value': 78,
                        },
                    ],
                    'randomize_ratio': 1.2,
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': [
                "'randomize_ratio' not in allowed [0, 1] range detected",
            ],
        }
