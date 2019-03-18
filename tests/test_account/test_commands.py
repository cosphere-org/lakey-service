
from datetime import datetime, timedelta
import json
from uuid import uuid1

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from lily.base.test import Client
import pytest
from freezegun import freeze_time

from account.models import AuthRequest, Account
from account.token import AuthToken
from tests.factory import EntityFactory


ef = EntityFactory()


class AuthenticateUICommandsTestCase(TestCase):

    def get_uri(self, request_uuid):
        return reverse(
            'account:auth.requests.authenticate.ui',
            kwargs={'request_uuid': request_uuid})

    def setUp(self):
        ef.clear()

        self.app = Client()

    def test_get(self):

        response = self.app.get(self.get_uri('some-uuid'))

        assert response.status_code == 200
        html = response.content.decode('utf8')
        assert 'some-uuid' in html
        assert html.strip().startswith('<!DOCTYPE html>')


class AuthRequestCommandsTestCase(TestCase):

    uri = reverse('account:auth.requests')

    def setUp(self):
        ef.clear()

        self.app = Client()

    def test_post(self):

        assert AuthRequest.objects.count() == 0

        response = self.app.post(self.uri)

        assert response.status_code == 201
        assert AuthRequest.objects.count() == 1
        r = AuthRequest.objects.all().first()
        assert response.json() == {
            '@event': 'AUTH_REQUEST_CREATED',
            '@type': 'auth_request',
            'authenticate_ui_uri': (
                '/accounts/auth_requests/{}/authenticate/ui/'.format(
                    str(r.uuid))),
            'request_uuid': str(r.uuid),
        }


class AuthRequestAttachAccountCommandsTestCase(TestCase):

    uri = reverse('account:auth.requests.attach_account')

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

        self.app = Client()

    def test_post(self):

        r = ef.auth_request()
        self.mocker.patch.object(
            AuthRequest,
            'get_oauth2_email'
        ).return_value = 'jacky@somewhere.org'

        assert Account.objects.count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'request_uuid': str(r.uuid),
                'oauth_token': 'some-oauth-token',
                'email': 'jacky@somewhere.org',
            }),
            content_type='application/json')

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'ACCOUNT_TO_AUTH_REQUEST_ATTACHED',
            '@type': 'empty',
        }
        assert Account.objects.count() == 1
        a = Account.objects.all().first()
        assert a.email == 'jacky@somewhere.org'

    def test_post__broken_body(self):

        self.mocker.patch.object(
            AuthRequest,
            'get_oauth2_email'
        ).return_value = 'jacky@somewhere.org'

        assert Account.objects.count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'request_uuid': 'some-uuid',
                'email': 'jacky@somewhere.org',
            }),
            content_type='application/json')

        assert response.status_code == 400
        assert response.json() == {
            '@event': 'BODY_DID_NOT_VALIDATE',
            '@type': 'error',
            'errors': {
                'oauth_token': ['This field is required.'],
                'request_uuid': ['"some-uuid" is not a valid UUID.'],
            },
        }
        assert Account.objects.count() == 0

    def test_post__request_does_not_exist(self):

        assert Account.objects.count() == 0

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'request_uuid': str(uuid1()),
                'oauth_token': 'some-auth-token',
                'email': 'jacky@somewhere.org',
            }),
            content_type='application/json')

        assert response.status_code == 404
        assert response.json() == {
            '@event': 'COULD_NOT_FIND_AUTHREQUEST',
            '@type': 'error',
        }
        assert Account.objects.count() == 0


class AuthTokenCommandsTestCase(TestCase):

    uri = reverse('account:auth.auth_token')

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()

        self.app = Client()

    def test_post(self):

        self.mocker.patch.object(
            AuthToken,
            'encode'
        ).return_value = 'fd78cd7d87f'

        r = ef.auth_request()
        r.account = ef.account()
        r.save()

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'request_uuid': str(r.uuid),
            }),
            content_type='application/json')

        assert response.status_code == 201
        assert response.json() == {
            '@event': 'AUTH_TOKEN_CREATED',
            '@type': 'auth_token',
            'token': 'fd78cd7d87f',
        }

    @override_settings(AUTH_REQUEST_EXPIRATION_DELTA=timedelta(seconds=120))
    @freeze_time('2014-10-10 12:00:00')
    def test_post_expired(self):

        r = ef.auth_request()
        r.account = ef.account()
        r.created_datetime = timezone.make_aware(
            datetime(2014, 10, 10, 11, 57, 0))
        r.save()

        response = self.app.post(
            self.uri,
            data=json.dumps({
                'request_uuid': str(r.uuid),
            }),
            content_type='application/json')

        assert response.status_code == 400
        assert response.json() == {
            '@event': 'EXPIRED_AUTH_REQUEST_DETECTED',
            '@type': 'error',
        }
