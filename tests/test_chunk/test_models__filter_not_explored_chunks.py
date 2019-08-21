
from django.test import TestCase

from tests.factory import EntityFactory

from chunk.models import Chunk
from chunk.models import NoChunksDetected

ef = EntityFactory()

class ChunkManagerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def ci(self, overrides=None):

        if overrides is None:
            overrides = [{}, {}]

        return ef.catalogue_item(spec=[
            {
                'name': 'A',
                'type': 'INTEGER',
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

    def d(self, overrides=None, spec=None, catalogue_item=None):

        if overrides is None:
            overrides = [{}, {}]

        return ef.download_request(
            created_by=ef.account(),
            # chunks=,
            spec=spec or {
                'columns': ['A'],
                'filters': [
                    {
                        'name': 'A',
                        'operator': '>=',
                        'value': 2,
                    },
                ],
                'randomize_ratio': 1,
            },
            catalogue_item=catalogue_item,
        )

    def test_simple_creation(self):
        ci = self.ci()
        c = self.c(catalogue_item=ci)
        d = self.d(catalogue_item=ci)

    def test_download_request_chunks(self):
        ci = self.ci()
        c1 = self.c(catalogue_item=ci)
        c2 = self.c(
            catalogue_item=ci,
            borders= [
                {
                    'column': 'A',
                    'minimum': 30,
                    'maximum': 35,
                    'distribution': None,
                },
                {
                    'column': 'B',
                    'minimum': 40,
                    'maximum': 45,
                    'distribution': None,
                },
            ],
        )
        c3 = self.c(
            catalogue_item=ci,
            borders= [
                {
                    'column': 'A',
                    'minimum': 50,
                    'maximum': 55,
                    'distribution': None,
                },
                {
                    'column': 'B',
                    'minimum': 60,
                    'maximum': 65,
                    'distribution': None,
                },
            ],
        )
        d = self.d(catalogue_item=ci)
        d.chunks.add(c1, c2)
        not_explored_chunks = Chunk.objects.filter_not_explored_chunks(1)
        import ipdb; ipdb.set_trace()