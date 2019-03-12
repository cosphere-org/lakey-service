
# from enum import Enum, unique

# from django.contrib.auth.models import User
# from django.db import models
# from lily.base.models import (
#     JSONSchemaField,
#     ValidatingModel,
#     number,
#     schema,
#     array,
#     boolean,
#     string,
#     object,
#     one_of,
#     enum,
# )

# from cataloger.models import CatalogItem


# def spec_validator(spec):

#     # FIXME: add some simple stuff here!!!! as example
#     # FIXME: column names must be right
#     # FIXME: operators work only for certain column types
#     # ..
#     pass


# class DownloadProcess(ValidatingModel):

#     #
#     # Version Control
#     #
#     created_datetime = models.DateTimeField(auto_now_add=True)

#     updated_datetime = models.DateTimeField(auto_now=True)

#     #
#     # Authorship
#     #
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     #
#     # SPEC
#     #
#     @unique
#     class FilterOperatorsEnum(Enum):

#         GREATER_THAN = '>'

#         GREATER_THAN_EQUAL = '>='

#         SMALLER_THAN = '<'

#         SMALLER_THAN_EQUAL = '<='

#         EQUAL = '='

#         NOT_EQUAL = '!='

#     download_spec = JSONSchemaField(
#         schema=schema(
#             columns=array(
#                 object(
#                     name=string(),
#                     is_selected=boolean(),
#                 )),
#             filters=array(
#                 object(
#                     name=string(),
#                     operator=enum(
#                         list(FilterOperatorsEnum.__members__.values())),
#                     value=one_of(
#                         number(),
#                         string()))),
#             randomize_ratio=number()),
#         validators=[spec_validator])

#     download_uri = models.URLField()

#     download_real_size = models.IntegerField()

#     download_estimated_size = models.IntegerField()

#     #
#     # CATALOGER / EXECUTOR
#     #
#     catalog_item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE)

#     executor_job_id = models.CharField(max_length=256)
