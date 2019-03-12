
# from django.test import TestCase

# from account.serializers import (
#     CatalogueItemSerializer,
#     CatalogueItemListSerializer,
# )
# from tests.factory import EntityFactory


# ef = EntityFactory()


# class CatalogueItemSerializerTestCase(TestCase):

#     def setUp(self):
#         ef.clear()

#     def test_serialize(self):

#         a = ef.account()
#         i = ef.catalogue_item()

#         assert CatalogueItemSerializer(i).data == {
#             '@type': 'catalogue_item',
#         }


# class CatalogueItemListSerializerTestCase(TestCase):

#     def setUp(self):
#         ef.clear()

#     def test_serialize(self):

#         a = ef.account()
#         i_0 = ef.catalogue_item()
#         i_1 = ef.catalogue_item()

#         assert CatalogueItemListSerializer({
#             'items': [i_0, i_1]
#         }).data == {
#             '@type': 'catalogue_items_list',
#             'items': [
#                 CatalogueItemSerializer(i_0).data,
#                 CatalogueItemSerializer(i_1).data,
#             ],
#         }
