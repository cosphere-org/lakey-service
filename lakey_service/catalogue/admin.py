
from django.contrib import admin
from .models import CatalogueItem


class CatalogueItemAdmin(admin.ModelAdmin):

    model = CatalogueItem

    list_display = ('name',)


admin.site.register(CatalogueItem, CatalogueItemAdmin)
