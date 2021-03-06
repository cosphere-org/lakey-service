
from lily import serializers

from .models import DownloadRequest
from account.serializers import AccountSerializer
from catalogue.serializers import CatalogueItemSerializer


class OperatorsPerColumnSerializer(serializers.Serializer):

    _type = 'column_operators'

    name = serializers.CharField()

    operators = serializers.ListField(child=serializers.CharField())


class DownloadRequestEstimateSerializer(serializers.Serializer):

    _type = 'download_request_estimated_size'

    estimated_size = serializers.IntegerField()


class DownloadRequestSerializer(serializers.ModelSerializer):

    _type = 'download_request'

    created_by = AccountSerializer()

    catalogue_item = CatalogueItemSerializer()

    class Meta:
        model = DownloadRequest

        fields = (
            # -- model fields
            'spec',
            'download_uri',
            'blob_name',
            'real_size',
            'estimated_size',
            'executor_job_id',
            'catalogue_item',
            'created_by',
            'is_cancelled',
        )


class DownloadRequestListSerializer(serializers.Serializer):

    _type = 'download_requests_list'

    requests = DownloadRequestSerializer(many=True)
