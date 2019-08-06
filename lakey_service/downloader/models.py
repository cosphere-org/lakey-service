
from enum import Enum, unique

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.db import models

from lily.base.models import (
    array,
    boolean,
    enum,
    JSONSchemaField,
    number,
    object,
    one_of,
    string,
    ValidatingModel,
)

from account.models import Account
from catalogue.models import CatalogueItem
from chunk.models import Chunk



class DownloadRequestManager(models.Manager):

    def simplify_spec(self, spec):
        filters_values = {}
        for spec_filter in spec['filters']:
            if spec_filter['name'] not in filters_values:
                filters_values[spec_filter['name']] = {}
            if spec_filter['operator'] not in filters_values[spec_filter['name']]:
                filters_values[spec_filter['name']][spec_filter['operator']] = []
            filters_values[spec_filter['name']][spec_filter['operator']].append(spec_filter['value'])

        for col_name in filters_values:
            if '<' and '<=' in filters_values[col_name]:
                filters_values[col_name]['<'].extend(filters_values[col_name]['<='])
                del filters_values[col_name]['<=']
            if '>' and '>=' in filters_values[col_name]:
                filters_values[col_name]['>'].extend(filters_values[col_name]['>='])
                del filters_values[col_name]['>=']

        s_s = {**spec, 'filters': []}
        for col_name in filters_values:
            for operator_name in filters_values[col_name]:
                values = filters_values[col_name][operator_name]

                if not len(values) > 0:
                    s_s['filters'].append({'name': col_name, 'operator': operator_name, 'value': values[0]})
                else:
                    if operator_name == '=':
                        s_s['filters'].append({'name': col_name, 'operator': operator_name, 'value': values[0]})
                    elif operator_name == ('>' or '>='):
                        s_s['filters'].append({'name': col_name, 'operator': operator_name, 'value': max(values)})
                    elif operator_name == ('<' or '<='):
                        s_s['filters'].append({'name': col_name, 'operator': operator_name, 'value': min(values)})

        return s_s

    def estimate_size(self, spec, catalogue_item_id):
        c_i = CatalogueItem.objects.get(id=catalogue_item_id)
        c_i_cols = [col['name'] for col in c_i.spec]
        spec = self.simplify_spec(spec)

        query = {}
        for spec_filter in self.simplify_spec(spec)['filters']:
            border_index_by_col_name = c_i_cols.index(spec_filter['name'])

            if spec_filter['operator'] == '<':
                query[f'borders__{border_index_by_col_name}__maximum__lt'] = spec_filter['value']
            elif spec_filter['operator'] == '<=':
                query[f'borders__{border_index_by_col_name}__maximum__lte'] = spec_filter['value']
            elif spec_filter['operator'] == '>':
                query[f'borders__{border_index_by_col_name}__minimum__gt'] = spec_filter['value']
            elif spec_filter['operator'] == '>=':
                query[f'borders__{border_index_by_col_name}__minimum__gte'] = spec_filter['value']
            elif spec_filter['operator'] == '=':
                query[f'borders__{border_index_by_col_name}__minimum__gte'] = spec_filter['value']
                query[f'borders__{border_index_by_col_name}__maximum__lte'] = spec_filter['value']

        filter_chunks = Chunk.objects.filter(catalogue_item_id=catalogue_item_id, **query)
        col_types_by_name = {col['name']: col['type'] for col in c_i.spec}

        return 0


class DownloadRequest(ValidatingModel):

    objects = DownloadRequestManager()

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
        on_delete=models.SET_NULL)

    #
    # Waiters
    #
    waiters = models.ManyToManyField(
        Account,
        related_name='download_requests_as_waiter')

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

    column_type_to_operators = {
        CatalogueItem.ColumnType.INTEGER.value: [
            FilterOperator.GREATER_THAN.value,
            FilterOperator.GREATER_THAN_EQUAL.value,
            FilterOperator.SMALLER_THAN.value,
            FilterOperator.SMALLER_THAN_EQUAL.value,
            FilterOperator.EQUAL.value,
            FilterOperator.NOT_EQUAL.value,
        ],
        CatalogueItem.ColumnType.FLOAT.value: [
            FilterOperator.GREATER_THAN.value,
            FilterOperator.GREATER_THAN_EQUAL.value,
            FilterOperator.SMALLER_THAN.value,
            FilterOperator.SMALLER_THAN_EQUAL.value,
            FilterOperator.EQUAL.value,
            FilterOperator.NOT_EQUAL.value,
        ],
        CatalogueItem.ColumnType.STRING.value: [
            FilterOperator.GREATER_THAN.value,
            FilterOperator.GREATER_THAN_EQUAL.value,
            FilterOperator.SMALLER_THAN.value,
            FilterOperator.SMALLER_THAN_EQUAL.value,
            FilterOperator.EQUAL.value,
            FilterOperator.NOT_EQUAL.value,
        ],
        CatalogueItem.ColumnType.BOOLEAN.value: [
            FilterOperator.EQUAL.value,
            FilterOperator.NOT_EQUAL.value,
        ],
    }

    spec = JSONSchemaField(
        schema=object(
            columns=array(
                string()),
            filters=array(
                object(
                    name=string(),
                    operator=enum(*[o.value for o in FilterOperator]),
                    value=one_of(
                        number(),
                        string(),
                        boolean()),
                    required=['name', 'operator', 'value'])),
            randomize_ratio=number(),
            required=['columns', 'filters']))

    normalized_spec = models.TextField(default='', blank=True)

    uri = models.URLField(null=True, blank=True)

    real_size = models.IntegerField(null=True, blank=True)

    estimated_size = models.IntegerField(null=True, blank=True)

    #
    # CATALOGER / EXECUTOR
    #
    catalogue_item = models.ForeignKey(
        CatalogueItem,
        on_delete=models.CASCADE,
        related_name='download_requests')

    executor_job_id = models.CharField(
        null=True,
        blank=True,
        max_length=256)

    is_cancelled = models.BooleanField(default=False)

    def clean(self):
        self.validate_spec_in_context_of_catalogue_item_spec()

    def validate_spec_in_context_of_catalogue_item_spec(self):
        """Validate spec using `CatalogueItem.spec`.

        - `spec.columns` must be taken from the list of registered columns
          as specified in `catalogue_item.spec`
        - `spec.filters[i].name` must be taken from the list of
          registered columns as specified in `catalogue_item.spec`
        - `spec.filters[i].operator` must be taken from the list of
          operators allowed for a column type
        - `spec.filters[i].value` must be of column type (or None is
          `is_nullable` was set)
        - `spec.randomize_ratio` must be in range [0, 1]

        """

        # -- only `catalogue_item.spec` columns are allowed
        # -- in `columns` and `filters` sections
        allowed_columns = set([
            col['name']
            for col in self.catalogue_item.spec])
        columns = set(self.spec['columns'])

        if not columns:
            raise ValidationError(
                "at least one column must be specified in 'columns'")

        if len(self.spec['columns']) != len(columns):
            raise ValidationError(
                "columns must appear only once in 'columns'")

        col_is_nullable = {
            column_spec['name']: column_spec['is_nullable']
            for column_spec in self.catalogue_item.spec
        }
        col_types = {
            column_spec['name']: column_spec['type']
            for column_spec in self.catalogue_item.spec
        }

        filter_columns = set(f['name'] for f in self.spec['filters'])

        if not columns.issubset(allowed_columns):
            unknown_columns = columns - allowed_columns
            unknown_columns = ', '.join([f"'{c}'" for c in unknown_columns])  # noqa
            raise ValidationError(
                f"unknown columns in 'columns' detected: {unknown_columns}")

        if not filter_columns.issubset(allowed_columns):
            unknown_columns = filter_columns - allowed_columns
            unknown_columns = ', '.join([f"'{c}'" for c in unknown_columns])
            raise ValidationError(
                f"unknown columns in 'filters' detected: {unknown_columns}")

        filters = self.spec['filters']
        for f in filters:
            # -- operators in the filters must be valid ones
            operator = f.get('operator')
            name = f.get('name')
            value = f.get('value')

            if not operator or not name or not value:
                continue

            # -- types used in filter must correspond to the types of their
            # -- respectful columns in `catalogue_item.spec`
            col_type = col_types[name]
            col_python_type = (
                CatalogueItem.column_type_to_python_type[col_type])
            expected_types = (col_python_type,)
            if col_is_nullable[name]:
                expected_types += (type(None),)

            if not isinstance(value, expected_types):
                raise ValidationError(
                    f"column type and filter value type "
                    f"mismatch detected for column '{name}'")

            allowed_operators = self.column_type_to_operators[col_type]
            if operator not in allowed_operators:
                raise ValidationError(
                    f"operator '{operator}' not allowed for column '{name}' "
                    f"detected")

        # -- randomized_ratio must be in range [0, 1]
        randomize_ratio = self.spec.get('randomize_ratio')
        if not isinstance(randomize_ratio, float):
            return

        if randomize_ratio < 0 or randomize_ratio > 1:
            raise ValidationError(
                "'randomize_ratio' not in allowed [0, 1] range detected")

    @staticmethod
    def normalize_spec(spec):

        columns = ','.join(sorted(spec['columns']))
        filters = ','.join(sorted([
            f"{fltr['name']}{fltr['operator']}{fltr['value']}"
            for fltr in spec['filters']
        ]))

        randomize_ratio = spec.get('randomize_ratio', 1)
        return (
            f'columns:{columns}|'
            f'filters:{filters}|'
            f'randomize_ratio:{randomize_ratio}')

    def __str__(self):  # noqa
        return (
            f'{self.id} - '
            f'{self.created_by.email}: '
            f'requested {self.catalogue_item.name}')


def pre_save_flow(sender, instance, **kwargs):
    instance.normalized_spec = DownloadRequest.normalize_spec(instance.spec)


pre_save.connect(pre_save_flow, sender=DownloadRequest)
