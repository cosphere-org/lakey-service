from enum import Enum, unique

from django.db import models
from django.core.exceptions import ValidationError

from lily.base.models import (
    array,
    boolean,
    JSONSchemaField,
    null_or,
    number,
    object,
    one_of,
    enum,
    string,
    ValidatingModel,
)


def distribution_validator(borders):

    # temporary in liny validators before schema:
    if isinstance(borders, list):
        for border in borders:

            b_name = border.get('column')
            b_type = border.get('type')
            if not b_name or not b_type:
                continue

            distribution = border.get('distribution')
            if not distribution:
                continue

            # -- values in distribution must has correct type
            b_type_to_python_type = Chunk.column_type_to_python_type
            expected_types = (b_type_to_python_type[b_type],)

            if distribution:
                for entry in distribution:
                    if not isinstance(entry['value_min'], expected_types):
                        raise ValidationError(
                            f"column type and distribution value type "  # noqa
                            f"mismatch detected for column '{b_name}'")

                    if not isinstance(entry['value_max'], expected_types):
                        raise ValidationError(
                            f"column type and distribution value type "  # noqa
                            f"mismatch detected for column '{b_name}'")

            # -- values in distribution must be unique
            values_min = [entry['value_min'] for entry in distribution]
            values_max = [entry['value_max'] for entry in distribution]
            all_values = values_min + values_max
            if len(all_values) != len(set(all_values)):
                raise ValidationError(
                    f"not unique distribution values for column '{b_name}' "
                    "detected")

            # -- counts in distribution must be integers
            counts_are_ints = [
                isinstance(entry['count'], int) for entry in distribution]
            if not all(counts_are_ints):
                raise ValidationError(
                    f"not integers distribution counts for column '{b_name}' "
                    "detected")

            # distribution min max betwean chunk min max
            if distribution:
                if not border["minimum"] < border["distribution"]["value_min"] < border["maximum"]:
                    raise ValidationError(
                        f"not unique distribution values for column '{b_name}' "
                        "detected")



class Chunk(ValidatingModel):

    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

    catalogue_item = models.ForeignKey(
        'catalogue.CatalogueItem',
        on_delete=models.CASCADE,
        related_name='chunks')

    @unique
    class ColumnType(Enum):

        INTEGER = 'INTEGER'

        FLOAT = 'FLOAT'

        STRING = 'STRING'

        BOOLEAN = 'BOOLEAN'

        DATETIME = 'DATETIME'

    column_type_to_python_type = {
        ColumnType.INTEGER.value: int,
        ColumnType.FLOAT.value: float,
        ColumnType.STRING.value: str,
        ColumnType.DATETIME.value: str,
        ColumnType.BOOLEAN.value: bool,
    }

    borders = JSONSchemaField(
        schema=array(
            object(
                column=string(),
                type=enum(*[t.value for t in ColumnType]),
                minimum=one_of(number(), string()),
                maximum=one_of(number(), string()),
                distribution=null_or(
                    array(
                        object(
                            value_min=one_of(
                                number(),
                                string(),
                                boolean(),
                            ),
                            value_max=one_of(
                                number(),
                                string(),
                                boolean()
                            ),
                            count=number(),
                            required=['value_min', 'value_max', 'count'])
                    )
                ),
                required=['column', 'minimum', 'maximum', 'distribution'],
            )
        ),
        validators=[distribution_validator]
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

            if not borders_columns.issubset(ci_columns):
                raise ValidationError(
                    "borders columns do not match catalogue item")

            if not ci_columns.issubset(borders_columns):
                raise ValidationError(
                    "borders columns do not match catalogue item")

            for border in self.borders:

                border_minimum = border['minimum']
                border_maximum = border['maximum']
                border_column = border["column"]

                if border_minimum in [None, '']:
                    raise ValidationError("minimum can not be empty")

                for ci_col in self.catalogue_item.spec:
                    if border_column == ci_col["name"]:

                        if ci_col["distribution"]:
                            catalogue_item_minimum = ci_col[
                                "distribution"][0]["value_min"]

                            if border_minimum < catalogue_item_minimum:
                                raise ValidationError(
                                    'borders minimu has to be greater than'
                                    ' catalogue_item minimum')

                            catalogue_item_maximum = ci_col[
                                "distribution"][-1]["value_max"]

                            if border_maximum > catalogue_item_maximum:
                                raise ValidationError(
                                    'borders maximum has to be greater '
                                    'than catalogue_item maximum')

                if border_maximum in [None, '']:
                    raise ValidationError("maximum can not be empty")

                if border_minimum >= border_maximum:
                    raise ValidationError(
                        "maximum has to be greater than minimum")

        else:
            raise ValidationError(
                "chunk - borders must be created and type list")
