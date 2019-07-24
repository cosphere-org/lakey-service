
from django.db import models
from django.core.exceptions import ValidationError

from lily.base.models import (
    array,
    JSONSchemaField,
    number,
    object,
    one_of,
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

        if self.borders:

            allowed_columns = [
                col['name'] for col in self.catalogue_item.spec]

            if len(self.catalogue_item.spec) != len(self.borders):
                raise ValidationError(
                        f"borders have to have same number of entries"
                        " as catalogue_item.spec")

            for border in self.borders:
                column = border['column']
                minimum = border['minimum']
                maximum = border['maximum']

                if column is None or minimum is None or maximum is None:
                    continue

                if not column in allowed_columns:
                    raise ValidationError(
                        f"unknown column detected")

                if column == '' or column is None:
                    raise ValidationError(
                        f"column can not by empty")

                if minimum is None or minimum == '':
                    raise ValidationError(
                        f"minimum can not by empty")

                if maximum is None or maximum == '':
                    raise ValidationError(
                        f"minimum can not by empty")

                if border['minimum'] >= border['maximum']:
                    raise ValidationError(
                        f"maximum has to be greater than minimum")

            # if type(minimum).__name__ != self.catalogue_item.spec:
            #     raise ValidationError(
            #         f"minimum can not by empty")

        else:
            raise ValidationError(
                        f"chunk - borders must be created")

        ######min max value ?????????????#################
