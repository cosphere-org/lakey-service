
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

            allowed_columns = [
                col['name'] for col in self.catalogue_item.spec]

            if type(self.borders).__name__ == 'list':
            #this if is temporary becouse lily schema validation is done after this function

                for col in self.catalogue_item.spec:
                    is_in_borders = False
                    for bor in self.borders:
                        if bor['column'] == col['name']:
                            is_in_borders = True

                    if is_in_borders == False:
                        raise ValidationError(
                            "borders columns do not match catalogue item"
                            )

                for ind, border in enumerate(self.borders):
                    column = border['column']
                    minimum = border['minimum']
                    maximum = border['maximum']

                    if column is None or minimum is None or maximum is None:
                        continue

                    if not column in allowed_columns:
                        raise ValidationError(
                            f"unknown column detected")

                    if minimum == None or minimum == '':
                        raise ValidationError(
                            f"minimum can not by empty")

                    if self.catalogue_item.spec[ind]['distribution']:
                        if minimum != self.catalogue_item.spec[ind]['distribution'][0]['value_min']:
                            raise ValidationError(
                                f"minimum has to match catalogue_item minimum")
                    
                    if maximum == None or maximum == '':
                        raise ValidationError(
                            f"maximum can not by empty")

                    if self.catalogue_item.spec[ind]['distribution']:
                        if maximum != self.catalogue_item.spec[ind]['distribution'][-1]['value_max']:
                            raise ValidationError(
                                f"maximum has to match catalogue_item maximum")

                    if border['minimum'] >= border['maximum']:
                        raise ValidationError(
                            f"maximum has to be greater than minimum")
        
        else:
            raise ValidationError(
                        f"chunk - borders must be created")
