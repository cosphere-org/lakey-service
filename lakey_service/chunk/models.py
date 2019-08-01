
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


class Chunk(ValidatingModel):

    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

    catalogue_item = models.ForeignKey(
        'catalogue.CatalogueItem',
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

    count = models.IntegerField(default=None)

    def borders_per_column(self, column_name):
        for chunk_border in list(self.borders):
            if chunk_border['column'] == column_name:
                return chunk_border

    def clean(self):
        self.validate_borders_in_context_of_catalogue_item()

    def validate_borders_in_context_of_catalogue_item(self):

        if isinstance(self.borders, list):

            ci_columns = set([col["name"] for col in self.catalogue_item.spec])
            borders_columns = set([
                border["column"]
                for border in self.borders])

            # ??? ask: is that ok
            if not borders_columns.issubset(ci_columns):
                raise ValidationError(
                    "borders columns do not match catalogue item")

            if not ci_columns.issubset(borders_columns):
                raise ValidationError(
                    "borders columns do not match catalogue item")


            for border in self.borders:

                minimum = border['minimum']
                maximum = border['maximum']

                if minimum in [None, '']:
                    raise ValidationError("minimum can not be empty")

                #??? ask: assuming distribution is not required
                # if dist:
                #     if minimum < dist['value_min']:
                #         raise ValidationError(
                #             f"minimum has to match catalogue_item minimum")

                if maximum in [None, '']:
                    raise ValidationError("maximum can not be empty")

                #??? ask: assuming distribution is not required
                # if dist:
                #     if maximum > dist[-1]['value_max']:
                #         raise ValidationError(
                #             'maximum has to smaller than max of catalogue_item ' # noqa
                #             'distribution')

                if minimum >= maximum:
                    raise ValidationError(
                        "maximum has to be greater than minimum")

        else:
            raise ValidationError(
                "chunk - borders must be created and type list")
