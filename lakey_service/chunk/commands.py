
from lily import (
    command,
    Meta,
    name,
    Output,
    Access,
    HTTPCommands,
)

from .domains import CHUNKS
from .models import Chunk
from .serializers import ChunksNotExploredSerializer
from account.models import Account


class ChunksNotExploredCommands(HTTPCommands):

    @command(
        name=name.BulkRead('NOT_EXPLORED_CHUNKS'),

        meta=Meta(
            title='Filter and read all not explored yet chunks',
            domain=CHUNKS),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=ChunksNotExploredSerializer),
    )
    def get(self, request, catalogue_item_id):

        raise self.event.BulkRead({
            'not_explored_chunks': Chunk.objects.filter_not_explored_chunks(
                catalogue_item_id)
        })
