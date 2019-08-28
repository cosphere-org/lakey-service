import os

import djclick as click

from catalogue.models import CatalogueItem
from chunk.models import Chunk


@click.command()
def command():
    CatalogueItem.objects.all().delete()
    Chunk.objects.all().delete()

    base_path = os.path.dirname(__file__)
    raw_path = os.path.join(base_path, 'raw_data', '2_column.csv')

    ci = CatalogueItem(
        name='ci_0',
        data_path=raw_path,
        executor_type='LOCAL'
    )

    ci.update_spec()
    ci.save()





