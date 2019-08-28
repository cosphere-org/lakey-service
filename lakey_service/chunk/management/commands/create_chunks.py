
import os

import djclick as click
import pandas
from numpy import histogram

from chunk.models import Chunk
from catalogue.models import CatalogueItem
from downloader.executors.local import numpy_type_to_column_type


chunks = []


def division(loc_df, max_c, chunks_path, catalogue_item):
    global chunks

    col_to_slice = loc_df.var().idxmax()
    local_df = loc_df.sort_values(col_to_slice)
    count = local_df.index.size
    median = int(count / 2)

    if not count <= max_c:
        left_half_df = local_df.iloc[:median]
        division(left_half_df, max_c, chunks_path, catalogue_item)

        right_half_df = local_df.iloc[median:]
        division(right_half_df, max_c, chunks_path, catalogue_item)

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

        chunk_data_path = os.path.join(chunks_path, f'{len(chunks)}.parquet')  # noqa
        chunk = Chunk(
            catalogue_item=catalogue_item,
            borders=borders,
            data_path=chunk_data_path,
            count=0)
        chunks.append(chunk)
        loc_df.to_parquet(chunk_data_path, engine='pyarrow')
        return


@click.command()
@click.argument('catalogue_item_name')
def command(catalogue_item_name):

    base_path = os.path.dirname(__file__)

    c_i = CatalogueItem.objects.get(name=catalogue_item_name)

    raw_data_name, _ = os.path.splitext(os.path.basename(c_i.data_path))
    chunks_path = os.path.join(base_path, 'partional_data', raw_data_name)

    try:
        os.mkdir(chunks_path)

    except FileExistsError:
        pass

    global chunks
    chunks = []
    division(pandas.read_csv(c_i.data_path), 125000, chunks_path, c_i)
    Chunk.objects.bulk_create(chunks)
