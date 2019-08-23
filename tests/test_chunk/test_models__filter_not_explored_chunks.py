
from django.test import TestCase

from tests.factory import EntityFactory

# from chunk.models import Chunk

ef = EntityFactory()


class ChunkManagerTestCase(TestCase):

    def setUp(self):
        ef.clear()

        self.ci_0 = ef.catalogue_item(
            name='temperatures',
            spec=[
                {
                    'name': 'A',
                    'type': 'INTEGER',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
            ])

        self.borders = [
            {
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
                'distribution': None,
            },
        ]
        self.ch_0 = ef.chunk(catalogue_item=self.ci_0, borders=self.borders)
        self.ch_1 = ef.chunk(catalogue_item=self.ci_0, borders=self.borders)
        self.ch_2 = ef.chunk(catalogue_item=self.ci_0, borders=self.borders)  # noqa

        self.d_0 = ef.download_request(
            catalogue_item=self.ci_0,
            spec={
                'columns': ['A'],
                'filters': [
                    {
                        'name': 'A',
                        'operator': '>=',
                        'value': 2,
                    },
                ],
                'randomize_ratio': 1,
            })

    #
    # FIXME
    # SESJA Z DODAWANIEM TESTÓW
    #
    # def test_simple_creation(self):

    #     ci = self.ci_0
    #     c = self.ch_0
    #     d = self.d_0

    #     assert ci == self.ci_0
    #     assert c == self.ch_0
    #     assert d == self.d_0

    # def test_download_request_chunks(self):

    #     c1 = self.ch_0
    #     c2 = self.ch_1
    #     c3 = self.ch_2
    #     d = self.d_0
    #     d.chunks.add(c1, c3)

    #     assert d.chunks.first() == c1
    #     assert d.chunks.last() == c3

    # def test_download_request_chunks_filter_not_explored(self):

    #     ci = self.ci_0
    #     c1 = self.ch_1
    #     c2 = self.ch_2
    #     c3 = self.ch_3
    #     d = self.d_0
    #     d.chunks.add(c1, c3)

    #     assert Chunk.objects.filter_not_explored_chunks(ci.id) == c2

    # def test_d_r_chunks_filter_not_explored_all_not_included(self):
    #     pass

    # def test_d_r_chunks_filter_not_explored_all_included(self):
    #     pass

    # def test_d_r_chunks_filter_not_explored_included_not_corect(self):
    #     pass
