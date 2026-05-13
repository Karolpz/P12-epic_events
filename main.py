from models.base import Base, engine
from models import Collaborator, Client, Contract, Event
from utils.token import get_token, verify_token
from commands.auth_command import auth_command
from commands.menu_command import show_menu
from models.base import Base, engine, Session
from models.collaborators import RoleEnum


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session() as session:
    test_collab = Collaborator(
        employee_id="EMP001",
        name="Alice",
        email="alice@epic.io",
        role=RoleEnum.gestion
    )
    test_collab.set_password("password123")
    session.add(test_collab)
    session.commit()


if __name__ == "__main__":
    token = get_token()
    if token and verify_token(token):
        show_menu()
    else:
        auth_command()

