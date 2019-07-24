from django.db import models
import pandas
from chunk.models import Chunk


class CatalogueItemManager(models.Manager):
    def create_chunks(self, ci_id, max_count):
        ci = super().get_queryset().get(pk=ci_id)
        global_df = pandas.DataFrame(ci.sample)
        borders = []

        def division(local_df, max_count):
            col_to_slice = local_df.var().idxmax()
            local_df = local_df.sort_values(col_to_slice)
            count = local_df.index.size
            median = int(count / 2)

            if not count <= max_count:
                left_half_df = local_df.iloc[:median]
                division(left_half_df, max_count)

                right_half_df = local_df.iloc[median:]
                division(right_half_df, max_count)
            else:
                border = []
                for col_name in local_df:
                    col = local_df[col_name]
                    border.append([col.min(), col.max(), count, col_name])
                borders.append(border)
                return

        division(global_df, 3)

        chunks = []
        for border in borders:
            chunks.append(Chunk(catalogue_item=self, borders=border))
        Chunk.objects.bulk_create(chunks)

        print(Chunk.objects.all())