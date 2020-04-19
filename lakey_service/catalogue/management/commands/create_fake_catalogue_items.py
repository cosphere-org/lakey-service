
import json
import textwrap
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
def command(overwrite):  # pragma: no cover
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

    #
    # MANUALLY CREATED
    #
    items = [
        {
            'description': textwrap.dedent('''
                Device specific features which can be used to understand their
                behaviour in time.
            '''),
            'data_file': 'ares_v1_device_features.json',
        },
        {
            'description': textwrap.dedent('''
                Gateway features which can be used to understand the the
                behaviour, the availability and issues with the Gateway itself.
            '''),
            'data_file': 'ares_v1_gateway_features.json',
        },
        {
            'description': textwrap.dedent('''
                Installations data allowing one to understand the
                configuration and set up of the installations that are present
                in the system.
            '''),
            'data_file': 'atlas_v0_installations.json',
        },
    ]

    for item in items:
        description = item['description']

        with open(os.path.join(base_dir, 'items', item['data_file'])) as f:
            data = json.loads(f.read())

        name = data['name']
        spec = data['spec']
        executor_type = data['executor_type']

        ci, created = CatalogueItem.objects.get_or_create(
            name=name,
            defaults={
                'maintained_by': a,
                'spec': spec,
                'description': description,
                'executor_type': executor_type,
            })

        if not created and overwrite:
            ci.maintained_by = a
            ci.spec = spec
            ci.description = description
            ci.executor_type = executor_type
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
