import re

from django.db.models import Q
from lily import (
    command,
    Input,
    Meta,
    name,
    Output,
    parsers,
    serializers,
    Access,
    HTTPCommands,
)

from account.models import Account
from .domains import CATALOGUE
from .models import CatalogueItem
from .serializers import CatalogueItemListSerializer, CatalogueItemSerializer
from .parsers import CatalogueItemParser


class CatalogueItemCollectionCommands(HTTPCommands):

    @command(
        name=name.Create(CatalogueItem),

        meta=Meta(
            title='Create Catalogue Item',
            domain=CATALOGUE),

        access=Access(access_list=[Account.TYPES.ADMIN]),

        input=Input(body_parser=CatalogueItemParser),

        output=Output(serializer=CatalogueItemSerializer),
    )
    def post(self, request):

        raise self.event.Created(
            CatalogueItem.objects.create(
                created_by=request.access['account'],
                updated_by=request.access['account'],
                **request.input.body))

    class QueryParser(parsers.QueryParser):

        query = parsers.CharField(default=None)

        has_samples = parsers.BooleanField(default=None)

    @command(
        name=name.BulkRead(CatalogueItem),

        meta=Meta(
            title='Bulk Read Catalogue Items',
            domain=CATALOGUE),

        access=Access(access_list=Account.TYPES.ANY),

        input=Input(query_parser=QueryParser),

        output=Output(serializer=CatalogueItemListSerializer),
    )
    def get(self, request):

        query = request.input.query['query']

        has_samples = request.input.query['has_samples']

        if query:
            qs = Q()
            expression = re.compile(r'([\&\|\~])(\s+)')
            query = expression.sub('\\1', query)

            for word in query.split():
                if word[0] == '~':
                    qs = qs & ~Q(name__icontains=word[1:])

                elif word[0] == '&':
                    qs = qs & Q(name__icontains=word[1:])

                elif word[0] == '|':
                    qs = qs | Q(name__icontains=word[1:])

                else:
                    qs = qs | Q(name__icontains=word)

            items = CatalogueItem.objects.filter(qs)

        else:
            items = CatalogueItem.objects.all()

        if has_samples:
            items = items.exclude(sample=[])

        elif not has_samples and has_samples is not None:
            items = items.filter(sample=[])

        raise self.event.BulkRead({'items': items})


class CatalogueItemElementCommands(HTTPCommands):

    @command(
        name=name.Read(CatalogueItem),

        meta=Meta(
            title='Read Catalogue Item',
            domain=CATALOGUE),

        access=Access(access_list=Account.TYPES.ANY),

        output=Output(serializer=CatalogueItemSerializer),
    )
    def get(self, request, item_id):

        raise self.event.Read(CatalogueItem.objects.get(id=item_id))

    @command(
        name=name.Update(CatalogueItem),

        meta=Meta(
            title='Update Catalogue Item',
            domain=CATALOGUE),

        access=Access(access_list=[Account.TYPES.ADMIN]),

        input=Input(body_parser=CatalogueItemParser),

        output=Output(serializer=CatalogueItemSerializer),
    )
    def put(self, request, item_id):

        item = CatalogueItem.objects.get(id=item_id)
        for field, value in request.input.body.items():
            setattr(item, field, value)

        item.updated_by = request.access['account']
        item.save()

        raise self.event.Updated(item)

    @command(
        name=name.Delete(CatalogueItem),

        meta=Meta(
            title='Delete Catalogue Item',
            domain=CATALOGUE),

        access=Access(access_list=[Account.TYPES.ADMIN]),

        output=Output(serializer=serializers.EmptySerializer),
    )
    def delete(self, request, item_id):

        item = CatalogueItem.objects.get(id=item_id)
        not_cancelled_count = (
            item.download_requests.filter(is_cancelled=False).count())

        if not_cancelled_count:
            raise self.event.BrokenRequest(
                'NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED',
                data={
                    'item_id': int(item_id),
                    'not_cancelled_count': not_cancelled_count,
                })

        item.delete()

        raise self.event.Deleted()


class CatalogueItemSampleAndDistributionsCommands(HTTPCommands):

    @command(
        name=name.Execute(
            'WITH_SAMPLE_AND_DISTRIBUTION_UPDATE', CatalogueItem),

        meta=Meta(
            title='Update Catalogue Item with Samples and Distributions',
            domain=CATALOGUE),

        is_atomic=True,

        access=Access(access_list=[Account.TYPES.ADMIN]),

        output=Output(serializer=serializers.EmptySerializer),
    )
    def put(self, request, item_id):

        item = CatalogueItem.objects.get(id=item_id)
        item.update_samples_and_distributions()

        raise self.event.Executed()
