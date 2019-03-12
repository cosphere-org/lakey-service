
from lily import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    _type = 'account'

    email = serializers.SerializerMethodField()

    def get_email(self, instance) -> str:
        return instance.user.email

    class Meta:
        model = Account

        fields = (
            'id',
            'email',
            'type')


class AuthTokenSerializer(serializers.Serializer):
    _type = 'auth_token'

    token = serializers.CharField()


class AuthRequestSerializer(serializers.Serializer):

    _type = 'auth_request'

    authenticate_ui_uri = serializers.URLField()

    request_uuid = serializers.CharField()
