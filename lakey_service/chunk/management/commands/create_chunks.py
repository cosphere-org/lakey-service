import os

import djclick as click
import pandas
from numpy import histogram

from chunk.models import Chunk
from catalogue.models import CatalogueItem
from downloader.executors.local import numpy_type_to_column_type

@click.command()
@click.argument('catalogue_item_name')
def command(catalogue_item_name):
    c_i = CatalogueItem.objects.get(name=catalogue_item_name)
    global_df = pandas.read_csv(c_i.data_path)


    partional_data_path = (f'/home/skpk/PycharmProjects/lakey-service/'
                           f'lakey_service/chunk/'
                           f'management/commands/partional_data')
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
                hist_bins = 10
                hist = histogram(local_df[col_name], bins=hist_bins)
                hist_count = hist[0]
                hist_value_range = hist[1]

                borders.append({
                    'column': col_name,
                    'type': numpy_type_to_column_type[global_df.dtypes[col_name].name],  # noqa
                    'minimum': int(col.min()),
                    'maximum': int(col.max()),
                    'distribution': [
                        {
                            'value_min': int(hist_value_range[hist_idx]),
                            'value_max': int(hist_value_range[hist_idx + 1]),
                            'count': int(hist_count[hist_idx])
                        } for hist_idx in range(hist_bins)
                    ]
                })

            chunk_data_path = (
                f'{partional_data_path}/{raw_data_name}/{len(chunks)}.parquet')
            chunk = Chunk(catalogue_item=c_i, borders=borders,
                          data_path=chunk_data_path, count=0)
            chunks.append(chunk)
            loc_df.to_parquet(chunk_data_path, engine='pyarrow')
            return

    os.mkdir(f'{partional_data_path}/{raw_data_name}')
    division(global_df, 125000)
    Chunk.objects.bulk_create(chunks)
