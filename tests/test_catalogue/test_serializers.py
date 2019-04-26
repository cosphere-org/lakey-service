
from django.test import TestCase

from catalogue.serializers import (
    CatalogueItemSerializer,
    CatalogueItemListSerializer,
)
from account.serializers import AccountSerializer
from tests.factory import EntityFactory


ef = EntityFactory()


class CatalogueItemSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        a_0 = ef.account()
        a_1 = ef.account()

        ci = ef.catalogue_item(
            name='names',
            created_by=a_0,
            maintained_by=a_1,
            spec=[{
                'name': 'name',
                'type': 'STRING',
                'is_nullable': False,
                'size': None,
                'distribution': None,
            }],
            sample=[{'name': 'Jack'}],
            executor_type='ATHENA')

        assert CatalogueItemSerializer(ci).data == {
            '@type': 'catalogue_item',
            'id': ci.id,
            'created_by': AccountSerializer(a_0).data,
            'updated_by': None,
            'maintained_by': AccountSerializer(a_1).data,
            'name': 'names',
            'spec': [
                {
                    'name': 'name',
                    'type': 'STRING',
                    'is_nullable': False,
                    'size': None,
                    'distribution': None,
                },
            ],
            'sample': [{'name': 'Jack'}],
            'executor_type': 'ATHENA',
        }


class CatalogueItemListSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        a_0 = ef.account()
        a_1 = ef.account()
        ci_0 = ef.catalogue_item(maintained_by=a_0)
        ci_1 = ef.catalogue_item(maintained_by=a_1)

        assert CatalogueItemListSerializer({
            'items': [ci_0, ci_1]
        }).data == {
            '@type': 'catalogue_items_list',
            'items': [
                CatalogueItemSerializer(ci_0).data,
                CatalogueItemSerializer(ci_1).data,
            ],
        }
