
from io import StringIO
from time import sleep

from django.conf import settings
import boto3
import requests
import pandas as pd

from .base import Base

athena = boto3.client(
    'athena',
    region_name=settings.AWS_LAKEY_REGION,
    aws_access_key_id=settings.AWS_LAKEY_KEY_ID,
    aws_secret_access_key=settings.AWS_LAKEY_KEY_SECRET)


s3 = boto3.client(
    's3',
    region_name=settings.AWS_LAKEY_REGION,
    aws_access_key_id=settings.AWS_LAKEY_KEY_ID,
    aws_secret_access_key=settings.AWS_LAKEY_KEY_SECRET)


class AthenaExecutor(Base):

    def execute(self, download_request):

        query = self.compile_to_query(download_request)

        database = download_request.catalogue_item.name.split('.')[0]

        return self.execute_query(database, query)

    #
    # SAMPLING
    #
    def get_sample(self, catalogue_item):

        sample_size = settings.CATALOGUE_ITEMS_SAMPLE_SIZE

        return self.execute_to_df(
            catalogue_item.database,
            query=f'''
                SELECT
                    g.*
                FROM
                    {catalogue_item.table} AS g,
                    (
                        SELECT
                            COUNT(*) AS total

                        FROM {catalogue_item.table}
                    ) as f
                    WHERE rand() <= (1.2 * {sample_size} / f.total)
                    LIMIT {sample_size}
                ''').to_dict(orient='records')

    #
    # GET SIZE
    #
    def get_size(self, column_name, catalogue_item):

        data = self.execute_to_df(
            catalogue_item.database,
            query=f'''
                SELECT
                    SUM(LENGTH(CAST({column_name} AS VARCHAR))) AS size
                FROM {catalogue_item.table}
            ''').to_dict(orient='list')

        return data['size'][0]

    #
    # DISTRIBUTION
    #
    def get_distribution(
            self, column_name, column_type, column_is_enum, catalogue_item):

        ct = catalogue_item.ColumnType

        enum_types = [ct.BOOLEAN.value, ct.STRING.value, ct.DATETIME.value]
        if column_is_enum or column_type in enum_types:
            return self.get_distribution_enum(column_name, catalogue_item)

        elif column_type in [ct.INTEGER.value, ct.FLOAT.value]:
            return self.get_distribution_numerical(column_name, catalogue_item)

    def get_distribution_enum(self, column, catalogue_item):

        limit = settings.CATALOGUE_ITEMS_DISTRIBUTION_VALUE_LIMIT

        return self.execute_to_df(
            catalogue_item.database,
            query=f'''
                SELECT
                    {column} AS value,
                    COUNT({column}) AS count

                FROM
                    {catalogue_item.table}

                GROUP BY {column}
                ORDER BY count DESC
                LIMIT {limit}
            ''').to_dict(orient='records')

    def get_distribution_numerical(self, column, catalogue_item):

        bins_count = (
            settings.CATALOGUE_ITEMS_DISTRIBUTION_VALUE_BINS_COUNT)

        data = self.execute_to_df(
            catalogue_item.database,
            query=f'''
                SELECT
                    MIN({column}) AS min_,
                    MAX({column}) AS max_
                FROM
                    {catalogue_item.table}
            ''').to_dict(orient='list')

        min_ = data['min_'][0]
        max_ = data['max_'][0]
        spread = max_ - min_
        bins = self.execute_to_df(
            catalogue_item.database,
            query=f'''
                SELECT
                    g.bin AS value,
                    COUNT(g.bin) AS count
                FROM (
                    SELECT
                        {column},
                        FLOOR(
                            {bins_count} * ({column} - {min_}) / ({spread})
                        ) AS bin
                    FROM
                        {catalogue_item.table}
                    ) AS g
                GROUP BY g.bin
                ORDER BY g.bin
            ''').to_dict(orient='records')

        return [
            {
                'value': b['value'] * (spread / bins_count) + min_,
                'count': b['count'],
            }
            for b in bins]

    #
    # EXECUTE
    #
    def execute_to_df(self, database, query):

        uri = self.execute_query(database, query)

        response = requests.get(uri)

        return pd.read_csv(StringIO(response.content.decode('utf-8')))

    def execute_query(self, database, query):

        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': settings.AWS_LAKEY_RESULTS_LOCATION,
            })

        execution_id = response['QueryExecutionId']
        bucket = settings.AWS_S3_BUCKET
        region = settings.AWS_LAKEY_REGION

        uri = (
            f'https://s3.{region}.amazonaws.com/{bucket}'
            f'/results/{execution_id}.csv')

        # -- FIXME: temp solution for making the url public
        s3.put_object(
            Key=f'/results/{execution_id}.csv',
            Bucket=bucket,
            ACL='public-read')

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # the URL should be created by extra method on DEMAND!!!!
        # How would it be possible for the quicker download??
        # https://boto3.amazonaws.com/v1/documentation/api/latest/
        # reference/services/s3.html?highlight=s3#S3.
        # Client.generate_presigned_url

        # FIXME: test if range HEADER !!!! also works here!!!!

        # FIXME: make it smarter!!!
        # -- wait some time till the results will be available
        sleep(2)

        return uri
