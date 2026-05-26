from epicevent.models.base import Base, engine
from epicevent.models import Collaborator, Client, Contract, Event
from epicevent.utils.token import get_token, verify_token
from epicevent.commands.auth_command import login, logout
from epicevent.commands.collaborators_command import collaborators
from epicevent.models.base import Base, engine, Session
from epicevent.models.collaborators import RoleEnum
import click


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# with Session() as session:
#     test_collab = Collaborator(
#         employee_id="EMP001",
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

if __name__ == "__main__":
    cli()

