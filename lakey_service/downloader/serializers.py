
from lily import serializers

from .models import DownloadRequest
from account.serializers import AccountSerializer
from catalogue.serializers import CatalogueItemSerializer
from chunk.serializers import ChunkSerializer


class OperatorsPerColumnSerializer(serializers.Serializer):

    _type = 'column_operators'

    name = serializers.CharField()

    operators = serializers.ListField(child=serializers.CharField())


class DownloadRequestRenderSerializer(serializers.Serializer):

    _type = 'download_request_render'

    columns_operators = OperatorsPerColumnSerializer(many=True)


class DownloadRequestEstimateSerializer(serializers.Serializer):

    _type = 'download_request_estimated_size'

    estimated_size = serializers.IntegerField()


class DownloadRequestSerializer(serializers.ModelSerializer):

    _type = 'download_request'

    created_by = AccountSerializer()

    catalogue_item = CatalogueItemSerializer()

    chunks = ChunkSerializer(many=True)

    class Meta:
        model = DownloadRequest

        fields = (
            # -- model fields
            'id',
            'spec',
            'uri',
            'real_size',
            'estimated_size',
            'executor_job_id',
            'catalogue_item',
            'created_by',
            'is_cancelled',
            'chunks',
        )


class DownloadRequestListSerializer(serializers.Serializer):

    _type = 'download_requests_list'

    requests = DownloadRequestSerializer(many=True)
