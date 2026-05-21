import click
from models.base import Session
from models.collaborators import Collaborator, RoleEnum
from utils.token import get_token, verify_token

@click.group()
def collaborators():
    pass

@collaborators.command()
def list():
    valid_user = verify_token(get_token())
    if not valid_user:
        click.echo(click.style("Vous devez être connecté.", fg="red"))
        return
    
    with Session() as session:
        collabs = session.query(Collaborator).all()
        if not collabs:
            click.echo(click.style("Aucun collaborateur trouvé.", fg="yellow"))
            return
        
        click.echo(click.style("Liste des collaborateurs :", fg="green"))
        for collab in collabs:
            click.echo(f"- {collab.name} ({collab.email}) - Rôle: {collab.role.value}")