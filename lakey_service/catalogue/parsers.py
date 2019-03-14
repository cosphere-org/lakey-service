
from lily import parsers

from .models import CatalogueItem


class CatalogueItemParser(parsers.ModelParser):

    maintained_by_id = parsers.IntegerField()

    class Meta:
        model = CatalogueItem

        fields = (
            # -- model fields
            'name',
            'spec',
            'sample',
            'maintained_by_id',
            'executor_type',
        )
