from databricks_api import DatabricksAPI
from datetime import datetime
from django.conf import settings

from .baseexecutor import BaseExecutor


class DatabricksExecutor(BaseExecutor):

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
