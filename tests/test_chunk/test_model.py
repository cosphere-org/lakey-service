
from django.test import TestCase

from chunk.models import Chunk
from tests.factory import EntityFactory


ef = EntityFactory()


class ChunkTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_simple_creation(self):

        ci = ef.catalogue_item()

        c = Chunk.objects.create(
            catalogue_item=ci,
            borders={
                'A': [15, 15],
                'B': [0, -10],
            })

        assert c.catalogue_item == ci
        assert c.borders == {
            'A': [15, 15],
            'B': [0, -10],
        }
