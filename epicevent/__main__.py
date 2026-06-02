from epicevent.models.base import Base, engine
from epicevent.commands.auth_command import auth
from epicevent.commands.collaborators_command import collaborators
from epicevent.commands.client_command import clients
from epicevent.commands.contract_command import contracts
from epicevent.commands.event_command import events
from epicevent.models.base import Base, engine
import click


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

@click.group()
def cli():
    pass

cli.add_command(auth)

cli.add_command(collaborators)

cli.add_command(clients)

cli.add_command(contracts)

cli.add_command(events)

if __name__ == "__main__":
    cli()

