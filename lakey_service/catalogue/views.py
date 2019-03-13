
from django.views.generic import View
from lily import (
    command,
    Input,
    Meta,
    name,
    Output,
    parsers,
    serializers,
    Access,
)

from account.models import Account
from .domains import CATALOGUE
from .models import CatalogueItem
from .serializers import CatalogueItemListSerializer, CatalogueItemSerializer
from .parsers import CatalogueItemParser


class CatalogueItemCollectionView(View):

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
            CatalogueItem.objects.create(**request.input.body))

    class QueryParser(parsers.QueryParser):

        query = parsers.CharField(default=None)

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

        if query:
            # FIXME: @zibg this is where you enter.
            # 1. you must figure out which fields we want to search
            # 2. how we must parse the query
            # 3. and so on ...
            items = CatalogueItem.objects.filter(name__icontains=query)

        else:
            items = CatalogueItem.objects.all()

        raise self.event.BulkRead({'items': items})


class CatalogueItemElementView(View):

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
        item.delete()

        raise self.event.Deleted()
