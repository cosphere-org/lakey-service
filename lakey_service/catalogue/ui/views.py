
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View

from ..models import CatalogueItem
from account.authorizer import Authorizer


class CatalogueItemsCollectionView(View):

    def get(self, request):
        account = Authorizer([]).ui_authorize(request)

        items = CatalogueItem.objects.filter(
            Q(created_by=account) |
            Q(updated_by=account) |
            Q(maintained_by=account) |
            Q(researchers__id=account.id)
        ).order_by('name')

        return render(
            request,
            'catalogue_items_collection.html',
            {
                'items': items,
                'name': 'catalogue',
                'is_authenticated': True,
            })


class CatalogueItemElementView(View):

    def get(self, request, item_id):

        account = Authorizer([]).ui_authorize(request)

        item = CatalogueItem.objects.filter(id=item_id)
        item = item.filter(
            Q(created_by=account) |
            Q(updated_by=account) |
            Q(maintained_by=account) |
            Q(researchers__id=account.id)).distinct('id')
        item = item.get()

        return render(
            request,
            'catalogue_items_element.html',
            {
                'item': item,
                'is_authenticated': True,
            })
