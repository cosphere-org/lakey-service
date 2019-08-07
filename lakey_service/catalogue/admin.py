
from django.contrib import admin  # pragma: no cover
from .models import CatalogueItem  # pragma: no cover


class CatalogueItemAdmin(admin.ModelAdmin):  # pragma: no cover

    model = CatalogueItem

    list_display = ('name',)


admin.site.register(CatalogueItem, CatalogueItemAdmin)  # pragma: no cover
