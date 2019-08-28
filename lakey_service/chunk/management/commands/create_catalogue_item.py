import os

import djclick as click

from catalogue.models import CatalogueItem


@click.command()
@click.argument('catalogue_item_filename')
def command(catalogue_item_filename):

    base_path = os.path.dirname(__file__)
    raw_path = os.path.join(
        base_path,
        'raw_data',
        f'{catalogue_item_filename}.csv')  # noqa

    try:
        CatalogueItem.objects.get(name=catalogue_item_filename)

    except CatalogueItem.DoesNotExist:
        ci = CatalogueItem(
            name=catalogue_item_filename,
            data_path=raw_path,
            executor_type='LOCAL')

        ci.update_spec()
        ci.save()
