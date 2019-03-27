
import djclick as click

from ...models import Account
from ...token import AuthToken


@click.command()
@click.argument(
    'email',
    type=str)
def command(email):
    """Create auth token for a given account."""

    account = Account.objects.get(email=email)
    token = AuthToken.encode(account)

    click.secho(f"Auth Token: '{token}'", fg='green')
