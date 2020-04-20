
import json

from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View

from ..models import DownloadRequest
from catalogue.models import CatalogueItem
from account.authorizer import Authorizer


class DownloadRequestCreateView(View):

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
            'download_request_create.html',
            {
                'name': item.name,
                'columns': sorted([c['name'] for c in item.spec]),
                'column_name_to_type': json.dumps({
                    c['name']: c['type'] for c in item.spec
                }),
                'filters': range(0, 5),
                'catalogue_item_id': item.id,
                'is_authenticated': True,
            })


class DownloadRequestCollectionView(View):

    def get(self, request):
        account = Authorizer([]).ui_authorize(request)

        reqs = DownloadRequest.objects.filter(
            Q(created_by=account) |
            Q(waiters__id=account.id))
        reqs = reqs.select_related('catalogue_item')
        reqs = reqs.order_by('catalogue_item__name')

        return render(
            request,
            'download_request_collection.html',
            {
                'name': 'downloads',
                'is_authenticated': True,
                'download_requests': reqs,
            })


class DownloadRequestElementView(View):

    def get(self, request, downalod_request_id):

        account = Authorizer([]).ui_authorize(request)

        req = DownloadRequest.objects.filter(id=downalod_request_id)
        req = req.filter(
            Q(created_by=account) |
            Q(waiters__id=account.id)).distinct('id')
        req = req.get()

        return render(
            request,
            'download_request_element.html',
            {'download_request': req})
