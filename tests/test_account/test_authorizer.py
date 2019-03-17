
from unittest.mock import Mock

from django.test import TestCase
from lily.base.events import EventFactory
import pytest

from account.token import AuthToken
from account.authorizer import Authorizer
from account.models import Account

from tests.factory import EntityFactory


ef = EntityFactory()


class AuthorizerTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

    #
    # AUTHORIZE
    #
    def test_authorize(self):

        a = ef.account(type=Account.TYPES.RESEARCHER)
        self.mocker.patch.object(AuthToken, 'decode').return_value = a
        request = Mock(META={'HTTP_AUTHORIZATION': 'bearer token'})

        # -- raises nothing, just works fine
        authorized = Authorizer([
            Account.TYPES.RESEARCHER,
            Account.TYPES.ADMIN,
        ]).authorize(request)

        assert authorized == {'account': a}

    def test_authorize__no_header(self):

        request = Mock(META={})

        with pytest.raises(EventFactory.AuthError) as e:
            Authorizer([]).authorize(request)

        assert e.value.data == {
            '@event': 'COULD_NOT_FIND_AUTH_TOKEN',
            '@type': 'error',
        }

    def test_authorize__no_bearer(self):

        request = Mock(META={'HTTP_AUTHORIZATION': 'no_bearer token'})

        with pytest.raises(EventFactory.AuthError) as e:
            Authorizer([]).authorize(request)

        assert e.value.data == {
            '@event': 'COULD_NOT_FIND_AUTH_TOKEN',
            '@type': 'error',
        }

    def test_authorize__access_denied(self):

        a = ef.account(type=Account.TYPES.RESEARCHER)
        self.mocker.patch.object(AuthToken, 'decode').return_value = a
        request = Mock(META={'HTTP_AUTHORIZATION': 'bearer token'})

        with pytest.raises(EventFactory.AccessDenied) as e:
            Authorizer([Account.TYPES.ADMIN]).authorize(request)

        assert e.value.data == {
            '@event': 'ACCESS_DENIED',
            '@type': 'error',
        }
