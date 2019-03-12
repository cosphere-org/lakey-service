
from django.test import TestCase

from account.serializers import (
    AccountSerializer,
    AuthTokenSerializer,
    AuthRequestSerializer,
)
from tests.factory import EntityFactory


ef = EntityFactory()


class AccountSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        a = ef.account()

        assert AccountSerializer(a).data == {
            '@type': 'account',
            'id': a.id,
            'email': a.email,
            'type': a.type,
            'type': 'RESEARCHER',
        }


class AuthTokenSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        assert AuthTokenSerializer({'token': 'whatever'}).data == {
            '@type': 'auth_token',
            'token': 'whatever',
        }


class AuthRequestSerializerTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_serialize(self):

        assert AuthRequestSerializer({
            'authenticate_ui_uri': '/some/url/whatever',
            'request_uuid': 'some-uuid-123',
        }).data == {
            '@type': 'auth_request',
            'request_uuid': 'some-uuid-123',
            'authenticate_ui_uri': '/some/url/whatever',
        }
