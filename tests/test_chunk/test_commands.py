
from django.test import TestCase
from django.urls import reverse
from lily.base.test import Client

from account.models import Account
from account.token import AuthToken
from chunk.serializers import ChunksNotExploredSerializer
from tests.factory import EntityFactory


ef = EntityFactory()


class ChunksNotExploredCommandsTestCase(TestCase):

    def get_uri(self, catalogue_item_id):
        return reverse(
            'chunk:chunks.not_explored',
            kwargs={'catalogue_item_id': catalogue_item_id})

    def setUp(self):
        ef.clear()

        self.app = Client()
        self.account = ef.account(type=Account.AccountType.ADMIN)

        token = AuthToken.encode(self.account)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'  # noqa
        }

    #
    # READ
    #
    def test_get_200(self):

        ci_0 = ef.catalogue_item(
            name='temperatures',
            spec=[
                {
                    'name': 'A',
                    'type': 'INTEGER',
                    'is_nullable': True,
                    'is_enum': True,
                    'size': None,
                    'distribution': None,
                },
            ])

        borders = [
            {
                'column': 'A',
                'minimum': 10,
                'maximum': 15,
                'distribution': None,
            },
        ]
        ch_0 = ef.chunk(catalogue_item=ci_0, borders=borders)
        ch_1 = ef.chunk(catalogue_item=ci_0, borders=borders)
        ch_2 = ef.chunk(catalogue_item=ci_0, borders=borders)  # noqa

        d_0 = ef.download_request(
            catalogue_item=ci_0,
            spec={
                'columns': ['A'],
                'filters': [
                    {
                        'name': 'A',
                        'operator': '>=',
                        'value': 2,
                    },
                ],
                'randomize_ratio': 1,
            })
        d_0.chunks.add(ch_0, ch_1)

        response = self.app.get(
            self.get_uri(ci_0.id),
            **self.headers)

        assert response.status_code == 200
        assert response.json() == {
            '@event': 'NOT_EXPLORED_CHUNKS_BULK_READ',
            **ChunksNotExploredSerializer({
                'not_explored_chunks': [ch_2],
            }).data,
        }

    # def test_get_404(self):

    #     response = self.app.get(
    #         self.get_uri(69506),
    #         **self.headers)

    #     assert response.status_code == 404
    #     assert response.json() == {
    #         '@event': 'COULD_NOT_FIND_CATALOGUEITEM',
    #         '@type': 'error',
    #         '@access': {
    #             'account_id': self.account.id,
    #         },
    #     }
