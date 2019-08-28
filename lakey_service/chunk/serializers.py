
from lily import serializers

from .models import Chunk


class ChunkSerializer(serializers.ModelSerializer):

    _type = 'chunk'

    class Meta:

        model = Chunk

        fields = (
            # -- model fields
            'created_datetime',
            'updated_datetime',
            'catalogue_item',
            'data_path',
            'borders',
        )


class ChunksNotExploredSerializer(serializers.Serializer):

    _type = 'not_explored_chunks'

    not_explored_chunks = ChunkSerializer(many=True)
