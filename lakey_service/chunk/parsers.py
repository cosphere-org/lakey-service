
from lily import parsers

from .models import Chunk


class ChunkParser(parsers.ModelParser):

    class Meta:

        model = Chunk

        fields = (
            # -- model fields
            'borders',
            'requested_count'
        )
