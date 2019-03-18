
import djclick as click

from ...models import Account


@click.command()
@click.argument(
    'email',
    type=str)
@click.option(
    '--type',
    default=Account.TYPES.RESEARCHER,
    type=click.Choice(Account.TYPES.ANY))
def command(email, type):
    """Create account of a given type."""

    try:
        Account.objects.get(email=email)

    except Account.DoesNotExist:
        account = Account.objects.create(email=email, type=type)

    else:
        raise click.ClickException('Account with that email already exists')

    click.secho(
        f'Successfully create an account with email: {email} and type: {type}',
        fg='green')
