
import os

import boto3


athena = boto3.client(
    'athena',
    region_name=os.environ['AWS_LAKEY_REGION'],
    aws_access_key_id=os.environ['AWS_LAKEY_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_LAKEY_KEY_SECRET'])


s3 = boto3.client(
    's3',
    region_name=os.environ['AWS_LAKEY_REGION'],
    aws_access_key_id=os.environ['AWS_LAKEY_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_LAKEY_KEY_SECRET'])


# FIXME: !!!! data validation for Download Request -->
#    columns must be set --> UNIQUE!!!
#    filters must default to []
class AthenaExecutor:

    def execute(self, download_request):

        query = self.compile_to_query(download_request)

        return self.execute_query(download_request, query)

    def compile_to_query(self, download_request):

        table = download_request.catalogue_item.name
        spec = download_request.spec

        # -- COLUMNS
        columns = ', '.join(spec['columns'])

        # -- FILTERS
        filters_entries = []
        for f in spec['filters']:
            if isinstance(f['value'], str):
                filters_entries.append(
                    f"{f['name']} {f['operator']} '{f['value']}'")  # noqa

            else:
                filters_entries.append(
                    f"{f['name']} {f['operator']} {f['value']}")

        if filters_entries:
            filters_entries = ' AND '.join(filters_entries)
            filters = f'WHERE {filters_entries}'

        else:
            filters = ''

        # -- RANDOMIZATION
        if spec.get('randomize_ratio'):
            randomize_ratio = spec['randomize_ratio']
            if filters:
                filters += ' AND '

            else:
                filters = 'WHERE '

            filters += f'RAND() >= {randomize_ratio}'

        return (
            f'SELECT {columns} FROM {table} {filters}').strip()

    def execute_query(self, download_request, query):

        database = download_request.catalogue_item.name.split('.')[0]

        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': os.environ['AWS_LAKEY_RESULTS_LOCATION'],
            })

        execution_id = response['QueryExecutionId']
        bucket = os.environ['AWS_S3_BUCKET']
        region = os.environ['AWS_LAKEY_REGION']

        url = (
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
        # 'lakey', 'results/cd471422-ef8f-484f-801a-2c7f52f47d3b.csv'

        # FIXME: test if range also works here!!!!
        return url
