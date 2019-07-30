
from django.db import models
from lily.base.models import JSONSchemaField, ValidatingModel, object


class Chunk(ValidatingModel):

    catalogue_item = models.ForeignKey(
        'catalogue.CatalogueItem',
        on_delete=models.CASCADE,
        related_name='chunks')

    # FIXME: enrich the schema to reflect borders structure!!!!
    borders = JSONSchemaField(
        schema=object())

    # FIXME: test it!!!
    @property
    def borders_per_column(self):

        return {
            border['name']: border
            for border in self.borders
        }
