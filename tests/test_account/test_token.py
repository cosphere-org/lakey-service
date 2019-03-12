
from unittest.mock import Mock
from datetime import timedelta

from django.test import TestCase, override_settings
from freezegun import freeze_time
from lily.base.events import EventFactory
import pytest
import jwt

from account.token import AuthToken
from tests.factory import EntityFactory


ef = EntityFactory()


class AuthTokenTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

    #
    # ENCODE
    #
    @freeze_time('2018-11-11 10:12:12')
    @override_settings(
        AUTH_TOKEN_SECRET_KEY='my.secret',
        AUTH_TOKEN_EXPIRATION_DELTA=timedelta(seconds=120))
    def test_encode(self):

        assert AuthToken.encode(
            Mock(type='BOSS', user=Mock(id=18, email='jacky@gmail.com'))
        ) == (
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
            'eyJ1c2VyX2lkIjoxOCwiZW1haWwiOiJqYWNre'
            'UBnbWFpbC5jb20iLCJhY2NvdW50X3R5cGUiOi'
            'JCT1NTIiwiZXhwIjoxNTQxOTMxMjUyfQ.ZKuD'
            '4HjG0l2AyX0Y0pyOHzLhTwXfEGMW6W3gJ03Fhzg')

    #
    # DECODE
    #
    def test_decode(self):

        a = ef.account()
        self.mocker.patch.object(
            jwt,
            'decode'
        ).return_value = {
            'user_id': a.user.id,
            'email': a.user.email,
            'account_type': a.type,
        }

        assert AuthToken.decode('token') == a

    def test_decode__token_expired(self):

        self.mocker.patch.object(
            jwt, 'decode').side_effect = jwt.ExpiredSignature

        with pytest.raises(EventFactory.AuthError) as e:
            AuthToken.decode('token')

        assert e.value.data == {
            '@event': 'AUTH_TOKEN_EXPIRED',
            '@type': 'error',
            'user_id': None,
        }

    def test_decode__token_is_broken(self):

        self.mocker.patch.object(jwt, 'decode').side_effect = jwt.DecodeError

        # -- expired
        with pytest.raises(EventFactory.AuthError) as e:
            AuthToken.decode('token')

        assert e.value.data == {
            '@event': 'AUTH_TOKEN_WAS_BROKEN',
            '@type': 'error',
            'user_id': None,
        }

    def test_decode__broken_payload(self):

        self.mocker.patch.object(jwt, 'decode').return_value = {
            'no_user_id': 134,
            'email': 'jacky@gmail.com',
        }

        # -- expired
        with pytest.raises(EventFactory.AuthError) as e:
            AuthToken.decode('token')

        assert e.value.data == {
            '@event': 'AUTH_TOKEN_MISSING_FIELDS_DETECTED',
            '@type': 'error',
            'user_id': None,
        }

    def test_decode__account_does_not_exist(self):

        self.mocker.patch.object(jwt, 'decode').return_value = {
            'user_id': 134,
            'email': 'jacky@gmail.com',
            'account_type': 'BOSS',
        }
        request = Mock(META={'HTTP_AUTHORIZATION': 'bearer token'})

        # -- expired
        with pytest.raises(EventFactory.AuthError) as e:
            AuthToken.decode(request)

        assert e.value.data == {
            '@event': 'AUTH_TOKEN_MISSING_ACCOUNT',
            '@type': 'error',
            'user_id': None,
        }
