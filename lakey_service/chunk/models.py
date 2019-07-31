
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

    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

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

    count = models.IntegerField(default=None)

    def clean(self):
        self.validate_borders_in_context_of_catalogue_item()

    def validate_borders_in_context_of_catalogue_item(self):

        if self.borders:

            for entry in self.catalogue_item.spec:
                col = entry['name']
                dist = entry['distribution']

                try:
                    border = self.borders_by_col[col]

                except KeyError:
                    raise ValidationError(
                        "borders columns do not match catalogue item")

                minimum = border['minimum']
                maximum = border['maximum']

                if minimum in [None, '']:
                    raise ValidationError("minimum can not be empty")

                if minimum < dist[0]['value_min']:
                    raise ValidationError(
                        f"minimum has to match catalogue_item minimum")

                if maximum in [None, '']:
                    raise ValidationError("maximum can not be empty")

                if maximum > dist[-1]['value_max']:
                    raise ValidationError(
                        'maximum has to smaller than max of catalogue_item '
                        'distribution')

                if minimum >= maximum:
                    raise ValidationError(
                        "maximum has to be greater than minimum")

        else:
            raise ValidationError("chunk - borders must be created")
