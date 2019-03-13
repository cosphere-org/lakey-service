
from lily import serializers

from .models import CatalogueItem
from account.serializers import AccountSerializer


class CatalogueItemSerializer(serializers.ModelSerializer):

    _type = 'catalogue_item'

    created_by = AccountSerializer()

    updated_by = AccountSerializer()

    maintained_by = AccountSerializer()

    class Meta:
        model = CatalogueItem

        fields = (
            # -- model fields
            'name',
            'spec',
            'sample',
            'executor_type',
            'created_by',
            'updated_by',
            'maintained_by',
        )


class CatalogueItemListSerializer(serializers.Serializer):

    _type = 'catalogue_items_list'

    items = CatalogueItemSerializer(many=True)
