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

@collaborators.command()
def add():
    valid_user = verify_token(get_token())
    if not valid_user:
        click.echo(click.style("Vous devez être connecté.", fg="red"))
        return
    
    employee_id = click.prompt("ID de l'employé")
    name = click.prompt("Nom du collaborateur")
    email = click.prompt("Email du collaborateur")
    password = click.prompt("Mot de passe", hide_input=True)
    role = click.prompt("Rôle (gestion, commercial, support)", type=click.Choice([r.value for r in RoleEnum]))

    with Session() as session:
        if session.query(Collaborator).filter(Collaborator.email == email).first():
            click.echo(click.style("Un collaborateur avec cet email existe déjà.", fg="red"))
            return
        
        new_collab = Collaborator(employee_id=employee_id, name=name, email=email, role=RoleEnum(role))
        new_collab.set_password(password)
        session.add(new_collab)
        session.commit()
        click.echo(click.style(f"Collaborateur {name} ajouté avec succès !", fg="green"))