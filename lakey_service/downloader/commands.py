
from lily import (
    command,
    Input,
    Meta,
    name,
    Output,
    Access,
    serializers,
    HTTPCommands,
)

from account.models import Account
from catalogue.models import CatalogueItem
from .domains import DOWNLOAD_REQUESTS
from .models import DownloadRequest
from .serializers import (
    DownloadRequestRenderSerializer,
    DownloadRequestEstimateSerializer,
    DownloadRequestSerializer,
    DownloadRequestListSerializer,
)
from .parsers import DownloadRequestParser, DownloadRequestRenderParser


class DownloadRequestRenderCommands(HTTPCommands):

    @command(
        name=name.Execute('RENDER', 'DOWNLOAD_REQUEST_UI_DATA'),

        meta=Meta(
            title=(
                'Render data needed for the built up of the '
                'download request form on client side'),
            domain=DOWNLOAD_REQUESTS),

        input=Input(body_parser=DownloadRequestRenderParser),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=DownloadRequestRenderSerializer),
    )
    def post(self, request):

        ci = CatalogueItem.objects.get(
            id=request.input.body['catalogue_item_id'])

        columns_operators = []
        for column in ci.spec:
            columns_operators.append({
                'name': column['name'],
                'operators': (
                    DownloadRequest.column_type_to_operators[column['type']]),
            })

        raise self.event.Executed({
            'columns_operators': columns_operators,
        })


class DownloadRequestEstimateCommands(HTTPCommands):

    @command(
        name=name.Execute('ESTIMATE', 'SIZE_OF_DOWNLOAD_REQUEST'),

        meta=Meta(
            title='Estimate the size download based on the provided spec',
            domain=DOWNLOAD_REQUESTS),

        input=Input(body_parser=DownloadRequestParser),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=DownloadRequestEstimateSerializer),
    )
    def post(self, request):

        raise self.event.Executed({
            'estimated_size': DownloadRequest.objects.estimate_size(
                **request.input.body),
        })


class DownloadRequestCollectionCommands(HTTPCommands):

    @command(
        name=name.CreateOrRead(DownloadRequest),

        meta=Meta(
            title='Create Download Request',
            description='''
                Create a Download Request in a smart way meaning that:
                - if same `DownloadRequest` already exists do not start
                  another one. (FIXME: maybe just attach user to the
                  waiters list)
                -
            ''',
            domain=DOWNLOAD_REQUESTS),

        input=Input(body_parser=DownloadRequestParser),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=DownloadRequestSerializer),
    )
    def post(self, request):

        spec = request.input.body['spec']

        r, created = DownloadRequest.objects.get_or_create(
            normalized_spec=DownloadRequest.normalize_spec(spec),
            catalogue_item_id=request.input.body['catalogue_item_id'],
            defaults={
                'created_by': request.access['account'],
                'spec': spec,
            })

        r.waiters.add(request.access['account'])

        if created:
            r.execute()
            raise self.event.Created(r)

        else:
            raise self.event.Read(r)

    @command(
        name=name.BulkRead(DownloadRequest),

        meta=Meta(
            title='Bulk Read Download Requests which you are waiting for',
            domain=DOWNLOAD_REQUESTS),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=DownloadRequestListSerializer),
    )
    def get(self, request):

        requests = DownloadRequest.objects.filter(
            waiters__id=request.access['account'].id)

        raise self.event.BulkRead({'requests': requests})


class DownloadRequestElementCommands(HTTPCommands):

    @command(
        name=name.Read(DownloadRequest),

        meta=Meta(
            title='Read DownloadRequest one is waiting for',
            domain=DOWNLOAD_REQUESTS),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=DownloadRequestSerializer),
    )
    def get(self, request, request_id):

        raise self.event.Read(
            DownloadRequest.objects.get(
                waiters__id=request.access['account'].id,
                id=request_id))

    @command(
        name=name.Delete(DownloadRequest),

        meta=Meta(
            title='Creator can cancel request or remove himself from waiters',
            domain=DOWNLOAD_REQUESTS),

        access=Access(access_list=Account.AccountType.ANY),

        output=Output(serializer=serializers.EmptySerializer),
    )
    def delete(self, request, request_id):

        account = request.access['account']
        r = DownloadRequest.objects.get(id=request_id)
        r.waiters.remove(account)

        if r.waiters.count() == 0:
            r.is_cancelled = True
            r.save()

        raise self.event.Deleted()
