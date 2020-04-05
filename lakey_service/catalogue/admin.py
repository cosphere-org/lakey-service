
from django.contrib import admin
from .models import CatalogueItem


@admin.register(CatalogueItem)
class CatalogueItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'executor_type', 'maintained_by')
