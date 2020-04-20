
import djclick as click

from ...models import Account, AccountType


@click.command()
@click.argument(
    'email',
    type=str)
@click.option(
    '--type',
    default=AccountType.RESEARCHER.value,
    type=click.Choice([
        AccountType.RESEARCHER.value,
        AccountType.ADMIN.value,
    ]))
def command(email, type):
    """Create account of a given type."""

    try:
        Account.objects.get(email=email)

    except Account.DoesNotExist:
        Account.objects.create(email=email, type=type)

    else:
        raise click.ClickException('Account with that email already exists')

    click.secho(
        f'Successfully create an account with email: {email} and type: {type}',
        fg='green')
