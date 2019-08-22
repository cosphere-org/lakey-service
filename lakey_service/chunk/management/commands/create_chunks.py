import os

import djclick as click
import pandas

from chunk.models import Chunk
from catalogue.models import CatalogueItem

# TODO: Distribution, research
#
@click.command()
@click.argument('filename')
@click.argument('max_count')
@click.argument('catalogue_item_id')
def command(filename, max_count, catalogue_item_id):
    items_path = os.path.dirname(os.path.abspath(__file__))
    global_df = pandas.read_csv(f'{items_path}/raw_data/{filename}')

    c_i = CatalogueItem.objects.all().first()

    chunks_borders = []

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
            border = []
            for col_name in local_df:
                col = local_df[col_name]
                border.append([col.min(), col.max(), count, col_name])
            chunks_borders.append(border)
            return

    division(global_df, int(max_count))

    chunks = []
    # for chunk_borders in chunks_borders:
    #     chunks.append(
    #         Chunk(
    #             catalogue_item=c_i,
    #             borders=[
    #                 {
    #                     'column': chunk_borders[3],
    #                     'type': 'INTEGER',
    #                     'minimum': 0,
    #                     'maximum': 100,
    #                     ''
    #                 }
    #             ],
    #             count=chunk_borders[2],
    #         )
    #     )
    # Chunk.objects.bulk_create(chunks)


    for chunk_borders in chunks_borders:
        chunks.append(
            Chunk(
                catalogue_item=c_i,
                borders=[
                    {
                        'column': col,
                        'count': count,
                        'minimum': int(min_),
                        'maximum': int(max_),
                    }
                    for min_, max_, count, col in chunk_borders
                ]))
    Chunk.objects.bulk_create(chunks)