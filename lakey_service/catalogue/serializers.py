
from lily import serializers

from .models import CatalogueItem
from account.serializers import AccountSerializer


class CatalogueItemSerializer(serializers.ModelSerializer):

    _type = 'catalogue_item'

    maintained_by = serializers.SerializerMethodField()

    def get_maintained_by(self, instance) -> AccountSerializer:
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
            'maintained_by',
        )


class CatalogueItemListSerializer(serializers.Serializer):

    _type = 'catalogue_items_list'

    items = CatalogueItemSerializer(many=True)
