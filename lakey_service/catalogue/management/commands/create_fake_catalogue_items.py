
import os
from glob import glob

import djclick as click
import yaml

from account.models import Account
from catalogue.models import CatalogueItem


@click.command()
@click.option(
    '--overwrite',
    is_flag=True,
    default=False)
def command(overwrite):
    """Create fake Catalogue Items."""

    a = Account.objects.filter(type='ADMIN').first()

    base_dir = os.path.dirname(__file__)
    items_data_files = glob(os.path.join(base_dir, 'items', '*.yaml'))

    for items_data_file in items_data_files:
        with open(items_data_file, 'r') as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)

        name = data.pop('name')

        ci, created = CatalogueItem.objects.get_or_create(
            name=name,
            defaults={'maintained_by': a, **data})

        if not created and overwrite:
            for k, v in data.items():
                setattr(ci, k, v)
                ci.save()

        if created:
            click.secho(
                f'Successfully created CatalogueItem: {name}', fg='green')

        elif not created and not overwrite:
            click.secho(
                f'Successfully read CatalogueItem: {name}', fg='green')

        elif not created and overwrite:
            click.secho(
                f'Successfully updated CatalogueItem: {name}', fg='green')
