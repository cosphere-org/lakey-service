
from django.db import models
from lily.base.models import JSONSchemaField, ValidatingModel, object

from catalogue.models import CatalogueItem


class Chunk(ValidatingModel):

    catalogue_item = models.ForeignKey(
        CatalogueItem,
        on_delete=models.CASCADE,
        related_name='chunks')

    borders = JSONSchemaField(
        schema=object())
