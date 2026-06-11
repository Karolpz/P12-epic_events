from epicevent.models.base import Base, engine
from epicevent.commands.auth_command import login, logout
from epicevent.commands.collaborators_command import collaborators
from epicevent.commands.client_command import clients
from epicevent.commands.contract_command import contracts
from epicevent.commands.event_command import events
import click
import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0
)

# Test Sentry integration by triggering an error
# division_by_zero = 1 / 0

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# with Session() as session:
#     test_collab = Collaborator(
#         name="Alice",
#         email="alice@epic.io",
#         role=RoleEnum.gestion
#     )
#     test_collab.set_password("password123")
#     session.add(test_collab)
#     session.commit()

@click.group()
def cli():
    pass

cli.add_command(login)
cli.add_command(logout)

cli.add_command(collaborators)

cli.add_command(clients)

cli.add_command(contracts)

cli.add_command(events)



if __name__ == "__main__":
    cli()

