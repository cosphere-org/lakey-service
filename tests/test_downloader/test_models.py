
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError

import pytest
from freezegun import freeze_time

from downloader.models import DownloadRequest
from tests.factory import EntityFactory


ef = EntityFactory()


class DownloadRequestTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

        self.ci = ef.catalogue_item(
            spec=[
                {
                    'name': 'product',
                    'type': 'STRING',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'price',
                    'type': 'INTEGER',
                    'is_nullable': False,
                    'is_enum': False,
                    'size': None,
                    'distribution': None,
                },
                {
                    'name': 'available',
                    'type': 'BOOLEAN',
                    'is_nullable': False,
                    'is_enum': False,
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

    def test_broken_spec__empty_columns(self):

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': [],
                    'filters': [
                        {
                            'name': 'price',
                            'operator': '>=',
                            'value': 78,
                        },
                    ],
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': [
                "at least one column must be specified in 'columns'",
            ],
        }

    def test_broken_spec__not_unique_columns(self):

        with pytest.raises(ValidationError) as e:
            DownloadRequest.objects.create(
                created_by=ef.account(),
                spec={
                    'columns': ['price', 'price'],
                    'filters': [
                        {
                            'name': 'price',
                            'operator': '>=',
                            'value': 78,
                        },
                    ],
                },
                catalogue_item=self.ci)

        assert e.value.message_dict == {
            '__all__': [
                "columns must appear only once in 'columns'",
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

    #
    # NORMALIZE_SPEC
    #
    def test_normalize_spec__sorts_columns(self):

        assert DownloadRequest.normalize_spec({
            'columns': ['price', 'amount', 'name'],
            'filters': [],
            'randomize_ratio': 0.9,
        }) == 'columns:amount,name,price|filters:|randomize_ratio:0.9'

    def test_normalize_spec__sorts_filters(self):

        assert DownloadRequest.normalize_spec({
            'columns': ['price', 'amount', 'name'],
            'filters': [
                {'name': 'price', 'operator': '>=', 'value': 78},
                {'name': 'price', 'operator': '=', 'value': 23},
                {'name': 'name', 'operator': '=', 'value': 'jack'},
            ],
            'randomize_ratio': 0.6,
        }) == (
            'columns:amount,name,price|'
            'filters:name=jack,price=23,price>=78|'
            'randomize_ratio:0.6')

    def test_normalize_spec__no_randomize_ratio(self):

        assert DownloadRequest.normalize_spec({
            'columns': ['price', 'amount'],
            'filters': [{'name': 'price', 'operator': '>=', 'value': 78}],
        }) == 'columns:amount,price|filters:price>=78|randomize_ratio:1'

    #
    # DOWNLOAD URI
    #
    def test_download_uri__no_uri(self):

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            blob_name=None,
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

        assert d.download_uri is None

    @freeze_time('10.04.2020 13:34:12')
    @override_settings(
        AZURE_BLOB_STORAGE_ACCOUNT_NAME='dl1storage',
        AZURE_BLOB_STORAGE_CONTAINER='lakey',
        AZURE_BLOB_STORAGE_ACCOUNT_KEY='secret')
    def test_download_uri__existing_uri(self):

        generate_blob_sas = self.mocker.patch(
            'downloader.models.generate_blob_sas')
        generate_blob_sas.return_value = 'v=6576&sig=4637e6dsd76'

        a = ef.account()
        d = DownloadRequest.objects.create(
            created_by=a,
            blob_name='7/8/9/data.csv',
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

        assert d.download_uri == (
            'https://dl1storage.blob.core.windows.net/lakey/7/8/9/data.csv'
            '?v=6576&sig=4637e6dsd76')

    #
    # PRE_SAVE FLOW
    #
    def test_pre_save_flow(self):

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

        assert d.normalized_spec == (
            'columns:product|filters:price>=78|randomize_ratio:1')
