
from enum import Enum, unique

from account.models import Account
from django.db import models
from lily.base.models import (
    JSONSchemaField,
    ValidatingModel,
    number,
    schema,
    array,
    string,
    object,
    one_of,
    enum,
)


def spec_validator(spec):

    # FIXME: add some simple stuff here!!!! as example
    # FIXME: column names must be right
    # FIXME: operators work only for certain column types
    # ..
    pass


class CatalogueItem(ValidatingModel):

    #
    # Version Control
    #
    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

    #
    # Authorship
    #
    create_by = models.ForeignKey(
        Account,
        null=True,
        on_delete=models.SET_NULL,
        related_name='catalogue_item_as_creator')

    updated_by = models.ForeignKey(
        Account,
        null=True,
        on_delete=models.SET_NULL,
        related_name='catalogue_item_as_updater')

    maintained_by = models.ForeignKey(
        Account,
        null=True,
        on_delete=models.SET_NULL,
        related_name='catalogue_item_as_maintainer')

    #
    # SPEC
    #
    name = models.CharField(max_length=256)

    # FIXME: this must be validated as a part of the overall model validation
    # since I need access to the `spec` field !!!
    sample = JSONSchemaField(
        default=[],
        blank=True,
        schema=schema(
            array(
                object())))

    @unique
    class ColumnTypesEnum(Enum):

        INTEGER = 'INTEGER'

        STRING = 'STRING'

        BOOLEAN = 'BOOLEAN'

    spec = JSONSchemaField(
        schema=schema(
            array(
                object(
                    name=string(),
                    type=enum([(t.name, t.value) for t in ColumnTypesEnum]),
                    size=number(),
                    distribution=array(
                        object(
                            value=one_of(number(), string()),
                            count=number())),
                ))),
        validators=[spec_validator])

    #
    # EXECUTOR
    #
    @unique
    class ExecutorsEnum(Enum):

        DATABRICKS = 'DATABRICKS'

        ATHENA = 'ATHENA'

    executor_type = models.CharField(
        max_length=256,
        choices=[(e.name, e.value) for e in ExecutorsEnum])
