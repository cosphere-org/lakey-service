
from django.db import models
from django.core.exceptions import ValidationError

from lily.base.models import (
    array,
    JSONSchemaField,
    number,
    object,
    string,
    ValidatingModel,
)

from catalogue.models import CatalogueItem


class Chunk(ValidatingModel):

    catalogue_item = models.ForeignKey(
        CatalogueItem,
        on_delete=models.CASCADE,
        related_name='chunks')

    borders = JSONSchemaField(
        schema=array(
            object(
                column=string(),
                minimum=one_of(number(), string()),
                maximum=one_of(number(), string()),
                required=['column', 'minimum', 'maximum'],
                )
            )
        )

    #############fix is chunks list??????????
    def clean(self):
        self.validate_borders_in_context_of_catalogue_item()

    def validate_borders_in_context_of_catalogue_item(self):

        allowed_columns = [
            [col['name'] for col in self.catalogue_item.spec]
            ]

        for border in self.borders:
            column = border['column']

            if not column in allowed_columns:
                raise ValidationError(
                    f"unknown columns in 'columns' detected: {column}")

            if border['minimum'] >= border['maximum']:
                raise ValidationError(
                    f"maximum has to be greater than minimum")

        ######min max value ?????????????#################
