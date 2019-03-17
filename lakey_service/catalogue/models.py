
from enum import Enum, unique

from django.core.exceptions import ValidationError
from django.db import models
from lily.base.models import (
    array,
    boolean,
    enum,
    JSONSchemaField,
    null,
    null_or,
    number,
    object,
    one_of,
    string,
    ValidatingModel,
)

from account.models import Account


def spec_validator(spec):
    """Validate `CatalogueItem.spec`.

    - `spec[i].distribution` entries must have values that are of the same
      type as defined in `spec[i].type` (None is allowed is column is defined
      as `is_nullable`)
    - `spec[i].distribution` entries values must be unique
    - `spec[i].distribution` entries counts must be integers

    """

    for col_spec in spec:

        # -- HACK: the presence of those fields is enforced by another
        # -- schema validation that happens before this one kicks in, but
        # -- unfortunately when one validators fails it doesn't break the
        # -- validation but just reports its errors and another validator
        # -- is executed.
        col_name = col_spec.get('name')
        col_type = col_spec.get('type')
        col_is_nullable = col_spec.get('is_nullable')
        if not col_name or not col_type:
            continue

        distribution = col_spec.get('distribution')
        if not distribution:
            continue

        # -- values in distribution must has correct type
        col_type_to_python_type = CatalogueItem.column_type_to_python_type
        expected_types = (col_type_to_python_type[col_type],)
        if col_is_nullable:
            expected_types += (type(None),)

        for entry in distribution:
            if not isinstance(entry['value'], expected_types):
                raise ValidationError(
                    f"column type and distribution value type "
                    f"mismatch detected for column '{col_name}'")

        # -- values in distribution must be unique
        all_values = [entry['value'] for entry in distribution]
        if len(all_values) != len(set(all_values)):
            raise ValidationError(
                f"not unique distribution values for column '{col_name}' "
                "detected")

        # -- counts in distribution must be integers
        counts_are_ints = [
            isinstance(entry['count'], int) for entry in distribution]
        if not all(counts_are_ints):
            raise ValidationError(
                f"not integers distribution counts for column '{col_name}' "
                "detected")


class CatalogueItem(ValidatingModel):

    #
    # Version Control
    #
    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

    #
    # Authorship
    #
    created_by = models.ForeignKey(
        Account,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='catalogue_item_as_creator')

    updated_by = models.ForeignKey(
        Account,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='catalogue_item_as_updater')

    maintained_by = models.ForeignKey(
        Account,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='catalogue_item_as_maintainer')

    #
    # SPEC
    #
    name = models.CharField(max_length=256, unique=True)

    sample = JSONSchemaField(
        default=list,
        blank=True,
        schema=array(
            object()))

    @unique
    class ColumnType(Enum):

        INTEGER = 'INTEGER'

        FLOAT = 'FLOAT'

        STRING = 'STRING'

        BOOLEAN = 'BOOLEAN'

    column_type_to_python_type = {
        ColumnType.INTEGER.value: int,
        ColumnType.FLOAT.value: float,
        ColumnType.STRING.value: str,
        ColumnType.BOOLEAN.value: bool,
    }

    spec = JSONSchemaField(
        schema=array(
            object(
                name=string(),
                type=enum(*[t.value for t in ColumnType]),
                size=null_or(number()),
                is_nullable=boolean(),
                distribution=null_or(
                    array(
                        object(
                            value=one_of(
                                null(),
                                number(),
                                string(),
                                boolean()),
                            count=number(),
                            required=['value', 'count']))),
                required=[
                    'name',
                    'type',
                    'size',
                    'is_nullable',
                    'distribution',
                ],
            )),
        validators=[spec_validator])

    #
    # EXECUTOR
    #
    @unique
    class Executor(Enum):

        DATABRICKS = 'DATABRICKS'

        ATHENA = 'ATHENA'

    executor_type = models.CharField(
        max_length=256,
        choices=[(e.name, e.value) for e in Executor])

    def clean(self):
        self.validate_samples_in_context_of_spec()

    def validate_samples_in_context_of_spec(self):
        """Validate `samples` using `CatalogueItem.spec` info.

        - `sample` entries must have the same names as registered in `spec`
        - `sample` entries values must be the same as the ones registered in
          `spec` (if `is_nullable` was set to True also None is allowed)

        """

        if not self.sample:
            return

        to_python_type = CatalogueItem.column_type_to_python_type
        col_name_to_type = {
            column_spec['name']: to_python_type[column_spec['type']]
            for column_spec in self.spec
        }
        col_is_nullable = {
            column_spec['name']: column_spec['is_nullable']
            for column_spec in self.spec
        }

        # -- all sample entries should have the same names
        row_names = set.intersection(
            *[set(row.keys()) for row in self.sample])
        expected_names = set([
            column_spec['name'] for column_spec in self.spec])

        if row_names != expected_names:
            raise ValidationError(
                f"Sample column names and spec names are not identical")

        # -- take into account that some columns are nullable
        for i, row in enumerate(self.sample):
            for name, value in row.items():
                expected_types = (col_name_to_type[name],)
                if col_is_nullable[name]:
                    expected_types += (type(None),)

                if not isinstance(value, expected_types):
                    raise ValidationError(
                        f"column type and sample value type "
                        f"mismatch detected for row number {i} "
                        f"column '{name}'")
