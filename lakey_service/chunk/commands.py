
from lily import (
    command,
    Input,
    Meta,
    name,
    Output,
    Access,
    HTTPCommands,
)

from .domains import CHUNKS
from .models import Chunk
from .parsers import ChunkParser
from .serializers import ChunkSerializer
from account.models import Account


class ChunkRenderCommands(HTTPCommands):

    @command(
        name=name.Execute('RENDER', 'CHUNK_EXPLORATION_MAP'),

        meta=Meta(
            title=(
                "render map which shows what part of chunk_map have not"
                "been explored yet"),
            domain=CHUNKS),

        input=Input(body_parser=ChunkParser),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=ChunkSerializer),
    )
    def post(self, request):

        raise self.event.Executed({
            'chunk_exploration_map': Chunk.objects.exploration_map(
                **request.input.body)
        })
