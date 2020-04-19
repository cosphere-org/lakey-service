
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View

from ..models import DownloadRequest
from account.authorizer import Authorizer


class DownloadRequestCreateView(View):

    def get(self, request, item_id):

        # FIXEM: read the catalogue item and prefill with some
        # data item_id
        return render(
            request,
            'download_request_create.html',
            {})


class DownloadRequestCollectionView(View):

    def get(self, request):
        account = Authorizer([]).ui_authorize(request)

        items = DownloadRequest.objects.filter(
            Q(created_by=account) |
            Q(updated_by=account) |
            Q(maintained_by=account) |
            Q(researchers__id=account.id)
        ).order_by('name')

        return render(
            request,
            'download_request_collection.html',
            {'items': items})


class DownloadRequestElementView(View):

    def get(self, request, item_id):

        account = Authorizer([]).ui_authorize(request)

        item = DownloadRequest.objects.filter(id=item_id)
        item = item.filter(
            Q(created_by=account) |
            Q(updated_by=account) |
            Q(maintained_by=account) |
            Q(researchers__id=account.id)).distinct('id')
        item = item.get()

        return render(
            request,
            'download_request_element.html',
            {'item': item})
