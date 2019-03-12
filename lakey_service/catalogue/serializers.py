
from lily import serializers

from .models import CatalogueItem
from account.serializers import AccountSerializer


class CatalogueItemSerializer(serializers.ModelSerializer):

    _type = 'catalogue_item'

    maintainer = serializers.SerializerMethodField()

    def get_maintainer(self, instance) -> AccountSerializer:
        return AccountSerializer(instance).data

    class Meta:
        model = CatalogueItem

        fields = (
            # -- model fields
            'name',
            'spec',
            'sample',
            'executor_type',

            # -- derived fields
            'maintainer',
        )


class CatalogueItemListSerializer(serializers.Serializer):

    _type = 'catalogue_items_list'

    items = CatalogueItemSerializer(many=True)
