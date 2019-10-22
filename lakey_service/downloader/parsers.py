
from lily import parsers

from .models import DownloadRequest


class DownloadRequestRenderParser(parsers.Parser):

    catalogue_item_id = parsers.IntegerField()


class DownloadRequestParser(parsers.ModelParser):

    catalogue_item_id = parsers.IntegerField()

    class Meta:
        model = DownloadRequest

        fields = (
            # -- model fields
            'spec',
            'catalogue_item_id',
        )
