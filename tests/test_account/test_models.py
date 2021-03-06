
from datetime import datetime, timedelta

from django.test import TestCase, override_settings
from django.utils import timezone
from freezegun import freeze_time
import pytest
from lily.base.events import EventFactory

from account.models import Account, AuthRequest, AccountType
from account.token import AuthToken
from tests.factory import EntityFactory


ef = EntityFactory()


class AccountTestCase(TestCase):

    def setUp(self):
        ef.clear()

    def test_simple_create(self):

        a = Account.objects.create(
            email='jacky@some.io',
            type=AccountType.ADMIN.value)

        assert a.email == 'jacky@some.io'
        assert a.type == AccountType.ADMIN.value


class AuthRequestTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

    def test_simple_create(self):

        r = AuthRequest.objects.create()

        assert len(str(r.uuid)) == 36
        assert r.account is None

    #
    # ATTACH_ACCOUNT
    #
    def test_attach_account__account_does_not_exist(self):

        self.mocker.patch(
            'account.models.validate_token'
        ).return_value = 'jacky@somewhere.org'

        assert Account.objects.count() == 0

        r = ef.auth_request()
        r.attach_account('jacky@somewhere.org', 'auth.code')

        assert Account.objects.count() == 1
        r.refresh_from_db()
        assert r.account.email == 'jacky@somewhere.org'

    def test_attach_account__account_exists(self):

        self.mocker.patch(
            'account.models.validate_token'
        ).return_value = 'jacky@somewhere.org'

        account = ef.account(email='jacky@somewhere.org')

        r = ef.auth_request()
        r.attach_account('jacky@somewhere.org', 'auth.code')

        assert Account.objects.count() == 1
        r.refresh_from_db()
        assert r.account == account

    def test_attach_account__emails_mismatch(self):

        self.mocker.patch(
            'account.models.validate_token'
        ).return_value = 'alice@somewhere.org'

        r = ef.auth_request()

        with pytest.raises(EventFactory.BrokenRequest) as e:
            r.attach_account('jacky@somewhere.org', 'auth.code')

        assert e.value.data == {
            '@event': 'EMAIL_MISMATCH_DETECTED',
            '@type': 'error',
        }

    def test_attach_account__oauth_user_info_works(self):

        id_token = self.mocker.patch('account.models.id_token')
        id_token.verify_oauth2_token.return_value = {
            'iss': 'https://accounts.google.com',
            'email': 'jess@whatever.com',
        }

        r = ef.auth_request()
        r.attach_account('jess@whatever.com', 'oauth.token')

        assert Account.objects.count() == 1
        r.refresh_from_db()
        assert r.account == Account.objects.all().first()

    def test_attach_account__wrong_issuer(self):

        id_token = self.mocker.patch('account.models.id_token')
        id_token.verify_oauth2_token.return_value = {
            'iss': 'https://NOT.google.com',
            'email': 'jess@whatever.com',
        }

        r = ef.auth_request()

        with pytest.raises(EventFactory.Conflict) as e:
            r.attach_account('jess@whatever.com', 'oauth.token')

        assert e.value.data == {
            '@event': 'GOOGLE_OAUTH2_USER_INFO_ERROR_DETECTED',
            '@type': 'error',
        }
        assert Account.objects.count() == 0
        r.refresh_from_db()
        assert r.account is None

    #
    # EXPIRED
    #
    @override_settings(AUTH_REQUEST_EXPIRATION_DELTA=timedelta(seconds=120))
    @freeze_time('2014-10-10 12:00:00')
    def test_expired(self):

        r = ef.auth_request()
        r.created_datetime = timezone.make_aware(
            datetime(2014, 10, 10, 11, 57, 0))
        r.save()

        assert r.expired is True

        r.created_datetime = timezone.make_aware(
            datetime(2014, 10, 10, 11, 58, 1))
        r.save()

        assert r.expired is False

    #
    # GET_TOKEN_AND_DELETE
    #
    def test_get_token_and_delete(self):

        self.mocker.patch.object(
            AuthToken,
            'encode'
        ).return_value = 'fd78cd7d87f'
        r_0 = ef.auth_request(ef.account())
        r_1 = ef.auth_request()  # noqa

        assert AuthRequest.objects.all().count() == 2

        assert r_0.get_token_and_delete() == 'fd78cd7d87f'
        assert AuthRequest.objects.all().count() == 1
        assert AuthRequest.objects.filter(id=r_0.id).count() == 0
