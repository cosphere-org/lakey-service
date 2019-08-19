
from lily import serializers

from .models import Chunk


class ChunkSerializer(serializers.ModelSerializer):

    _type = 'chunk'

    class Meta:

        model = Chunk

        fields = (
            # -- model fields
            'created_datatime',
            'updated_datatime',
            'borders',
            'requested_time',
            'count',
        )
