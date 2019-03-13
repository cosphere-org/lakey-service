
from enum import Enum, unique

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

from account.models import Account
from cataloger.models import CatalogItem


def data_spec_validator(spec):

    # FIXME: add some simple stuff here!!!! as example
    # FIXME: column names must be right
    # FIXME: operators work only for certain column types
    # ..
    pass


class DownloadProcess(ValidatingModel):

    #
    # Version Control
    #
    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

    #
    # Authorship
    #
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    #
    # Data Related Fields
    #
    @unique
    class FilterOperator(Enum):

        GREATER_THAN = '>'

        GREATER_THAN_EQUAL = '>='

        SMALLER_THAN = '<'

        SMALLER_THAN_EQUAL = '<='

        EQUAL = '='

        NOT_EQUAL = '!='

    data_spec = JSONSchemaField(
        schema=schema(
            columns=array(
                string()),
            filters=array(
                object(
                    name=string(),
                    operator=enum([o.value for o in FilterOperator]),
                    value=one_of(
                        number(),
                        string()))),
            randomize_ratio=number()),
        validators=[data_spec_validator])

    data_uri = models.URLField()

    data_real_size = models.IntegerField()

    data_estimated_size = models.IntegerField()

    #
    # CATALOGER / EXECUTOR
    #
    catalog_item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE)

    executor_job_id = models.CharField(max_length=256)
