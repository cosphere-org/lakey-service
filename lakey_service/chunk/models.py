
from django.db import models
from lily.base.models import JSONSchemaField, ValidatingModel, object


class Chunk(ValidatingModel):

    catalogue_item = models.ForeignKey(
        'catalogue.CatalogueItem',
        on_delete=models.CASCADE,
        related_name='chunks')