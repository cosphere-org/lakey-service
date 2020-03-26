import json
import requests

from databricks_api import DatabricksAPI
from datetime import datetime
from django.conf import settings


class DataBricksExecutor:

    def __init__(self):
        self.db = DatabricksAPI(
            host=settings.DATABRICKS_HOST,
            token=settings.DATABRICKS_TOKEN
        )

    def __generate_file_path(self):
        """ Return path of output file """
        now = datetime.now()
        output_location = settings.DATABRICKS_RESULTS_LOCATION
        filename = now.strftime("%Y%m%d-%H%M%S")

        return output_location+filename+"_output.csv"

    # TODO: DRY -> create BaseExecutor with virtual methods
    # raise NotImplemented() as default
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

    def execute(self, download_request):

        query = self.compile_to_query(download_request)

        return self.execute_query(query)

    def execute_query(self, query):
        output_file = self.__generate_file_path()

        self.db.jobs.submit_run(
            run_name='Lakey get data',
            existing_cluster_id=settings.DATABRICKS_CLUSTER_ID,
            spark_python_task={
                'python_file': settings.DATABRICKS_SCRIPT_LOCATION,
                'parameters': [query, output_file]
            }
        )

        # TODO return proper location of output file
        return settings.DATABRICKS_HOST
