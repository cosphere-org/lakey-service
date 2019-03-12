
from lily import parsers

from .models import CatalogueItem


class CatalogueItemParser(parsers.ModelParser):

    class Meta:
        model = CatalogueItem

        fields = (
            # -- model fields
            'name',
            'spec',
            'sample',
            'maintainer_user_id',
            'executor_type',
        )
