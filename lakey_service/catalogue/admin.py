
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
from django.contrib import admin

from .models import CatalogueItem


@admin.register(CatalogueItem)
class CatalogueItemAdmin(admin.ModelAdmin):

    list_display = ('name', 'executor_type', 'maintained_by')

    filter_horizontal = ('researchers',)

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

    fieldsets = (
        ('Users', {
            'fields': (
                'created_by',
                'updated_by',
                'maintained_by',
                'researchers',
            )
        }),
        ('Meta', {
            'fields': (
                'name',
                'description',
                'executor_type',
                'spec')
        }),

        ('Sample', {
            'classes': ('collapse',),
            'fields': (
                'sample',)
        }),
    )
