
class BaseExecutor:

    def execute(self, download_request):
        raise NotImplementedError()

    def get_sample(self, catalogue_item):
        raise NotImplementedError()

    def get_size(self, column_name, catalogue_item):
        raise NotImplementedError()

    def get_distribution(
            self, column_name, column_type, column_is_enum, catalogue_item):
        raise NotImplementedError()

    def compile_to_query(self, download_request):

        table = download_request.catalogue_item.name
        spec = download_request.spec

        # -- COLUMNS
        columns = ', '.join(spec['columns'])

        # -- FILTERS
        filters_entries = []
        for fltr in spec['filters']:
            if isinstance(fltr['value'], str):
                filters_entries.append(
                    f"{fltr['name']} {fltr['operator']} '{fltr['value']}'")  # noqa

            else:
                filters_entries.append(
                    f"{fltr['name']} {fltr['operator']} {fltr['value']}")

        if filters_entries:
            filters_entries = ' AND '.join(filters_entries)
            filters = f'WHERE {filters_entries}'

        else:
            filters = ''

        query = f'SELECT {columns} FROM {table} {filters}'

        # -- RANDOMIZATION
        if spec.get('randomize_ratio'):
            randomize_ratio = spec['randomize_ratio']

            query = f'''
                SELECT
                    q.*
                FROM ({query}) AS q
                WHERE RAND() >= {randomize_ratio}
            '''

        return query
