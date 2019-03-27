
from django.test import TestCase
from click.testing import CliRunner
import pytest

from account.management.commands.create_account import command
from account.models import Account
from tests.factory import EntityFactory


ef = EntityFactory()


class CreateAccountTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()
        self.runner = CliRunner()

    def test_command(self):

        assert Account.objects.count() == 0

        result = self.runner.invoke(
            command, ['jess@some.where', '--type', 'ADMIN'])

        assert result.exit_code == 0
        assert result.output.strip() == (
            "Successfully create an account with "
            "email: jess@some.where and type: ADMIN")
        assert Account.objects.count() == 1
        a = Account.objects.all().first()
        assert a.email == 'jess@some.where'
        assert a.type == 'ADMIN'

    def test_command__default_type(self):

        assert Account.objects.count() == 0

        result = self.runner.invoke(command, ['jess@some.where'])

        assert result.exit_code == 0
        assert result.output.strip() == (
            "Successfully create an account with "
            "email: jess@some.where and type: RESEARCHER")
        assert Account.objects.count() == 1
        a = Account.objects.all().first()
        assert a.email == 'jess@some.where'
        assert a.type == 'RESEARCHER'

    def test_command__account_exists(self):

        ef.account(email='jess@some.where')

        result = self.runner.invoke(command, ['jess@some.where'])

        assert result.exit_code == 1
        assert result.output.strip() == (
            "Error: Account with that email already exists")
