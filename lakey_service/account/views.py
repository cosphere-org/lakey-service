from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from catalogue.models import CatalogueItem


class DashboardView(ListView):
    model = CatalogueItem

    def get_queryset(self):
        return CatalogueItem.objects.filter(
            maintained_by__email=self.request.user.email).order_by('name')


@login_required
def catalogue_item_view(request, item_id):

    c_item = tag = get_object_or_404(CatalogueItem, id=item_id)

    if c_item.maintained_by.email != request.user.email:
        return HttpResponseForbidden('NOT_AUTHORIZED')

    return render(request,
                  'account/detailed.html',
                  {'catalogue_item': c_item})
