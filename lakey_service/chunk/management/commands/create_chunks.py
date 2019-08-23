import os

import djclick as click
import pandas
# from numpy import histogram

from chunk.models import Chunk
from catalogue.models import CatalogueItem


# TODO: Distribution, research
#
@click.command()
@click.argument('catalogue_item_name')
def command(catalogue_item_name):
    c_i = CatalogueItem.objects.get(name=catalogue_item_name)
    global_df = pandas.read_csv(c_i.data_path)

    types = {
        'int64': 'INTEGER'
    }
    partional_data_path = '/home/skpk/PycharmProjects/' \
                          'lakey-service/lakey_service/chunk/' \
                          'management/commands/partional_data'
    raw_data_name = c_i.data_path.split("/")[-1].split(".")[0]

    chunks = []

    def division(loc_df, max_c):
        col_to_slice = loc_df.var().idxmax()
        local_df = loc_df.sort_values(col_to_slice)
        count = local_df.index.size
        median = int(count / 2)

        if not count <= max_c:
            left_half_df = local_df.iloc[:median]
            division(left_half_df, max_c)

            right_half_df = local_df.iloc[median:]
            division(right_half_df, max_c)
        else:
            borders = []
            for col_name in local_df:
                col = local_df[col_name]
                # hist = histogram(local_df)
                borders.append({
                    'column': col_name,
                    'type': types[global_df.dtypes[col_name].name],
                    'minimum': col.min(),
                    'maximum': col.max(),
                    'distribution': [
                        # {
                        #     'value_min': value_min,
                        #     'value_max': value_max,
                        #     'count': count
                        # } for value_min, value_max, count in hist,
                    ]
                })

            chunk_data_path = (
                f'{partional_data_path}/{raw_data_name}/{len(chunks)}.parquet')  # noqa
            chunk = Chunk(
                catalogue_item=c_i,
                borders=borders,
                data_path=chunk_data_path)
            chunks.append(chunk)

            loc_df.to_parquet(chunk_data_path, engine='pyarrow')

    os.mkdir(f'{partional_data_path}/{raw_data_name}')
    division(global_df, 125000)
