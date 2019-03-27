
from unittest.mock import call

from django.test import TestCase
from click.testing import CliRunner
import pytest

from account.management.commands.create_auth_token import command
from account.token import AuthToken
from tests.factory import EntityFactory


ef = EntityFactory()


class CreateAuthTokenTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker):
        self.mocker = mocker

    def setUp(self):
        ef.clear()
        self.runner = CliRunner()

    def test_command(self):

        encode = self.mocker.patch.object(AuthToken, 'encode')
        encode.return_value = 'some.token.123'
        a = ef.account()

        result = self.runner.invoke(command, [a.email])

        assert result.exit_code == 0
        assert result.output.strip() == "Auth Token: 'some.token.123'"
        assert encode.call_args_list == [call(a)]
