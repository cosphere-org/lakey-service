
from enum import Enum, unique

from django.core.exceptions import ValidationError
from django.db import models
from lily.base.models import (
    JSONSchemaField,
    ValidatingModel,
    number,
    array,
    string,
    boolean,
    object,
    one_of,
    null_or,
    enum,
)

from account.models import Account


def spec_validator(spec):

    for column_spec in spec:
        # -- this must be addressed by top level schema validation
        column_name = column_spec.get('name')
        column_type = column_spec.get('type')
        if not column_name or not column_type:
            continue

        distribution = column_spec.get('distribution')
        if not distribution:
            continue

        to_python_type = CatalogueItem.column_type_to_python_type
        for col_type, col_python_type in to_python_type.items():
            if column_type == col_type:
                for entry in distribution:
                    if not isinstance(entry['value'], col_python_type):
                        raise ValidationError(
                            f"column type and distribution value type "
                            f"mismatch detected for column '{column_name}'")


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
        default=[],
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
                            value=one_of(number(), string(), boolean()),
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
