
import os

from databricks_api import DatabricksAPI
from django.conf import settings
from django.utils import timezone
from django.utils import crypto

from .base import BaseExecutor


class DatabricksExecutor(BaseExecutor):

    def __init__(self):
        self.db = DatabricksAPI(
            host=settings.DATABRICKS_HOST,
            token=settings.DATABRICKS_TOKEN
        )

    def get_output_file_path(self):

        filename = '_'.join([timezone.now().strftime("%Y%m%d-%H%M%S"),
                            crypto.get_random_string(length=4),
                            "output.csv"])

        return os.path.join(
            settings.DATABRICKS_RESULTS_LOCATION, filename)

    def execute(self, download_request):

        query = self.compile_to_query(download_request)

        return self.execute_query(query)

    def execute_query(self, query):

        output_file = self.get_output_file_path()

        self.db.jobs.submit_run(
            run_name='Lakey get data',
            existing_cluster_id=settings.DATABRICKS_CLUSTER_ID,
            spark_python_task={
                'python_file': settings.DATABRICKS_SCRIPT_LOCATION,
                'parameters': [query, output_file]
            }
        )

        return output_file.replace('/dbfs/mnt/', '')
