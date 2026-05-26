import click
from epicevent.models.base import Session
from epicevent.models.collaborators import Collaborator, RoleEnum
from epicevent.utils.token import get_token, verify_token
from epicevent.services.collaborators_service import CollaboratorsService

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
        service = CollaboratorsService(session)
        collabs = service.list_collaborators()
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
    password = click.prompt("Mot de passe", hide_input=True, confirmation_prompt=True)
    role = click.prompt("Rôle", type=click.Choice([r.value for r in RoleEnum]))

    with Session() as session:
        service = CollaboratorsService(session)
        new_collab = service.add_collaborator(employee_id, name, email, password, RoleEnum(role))
        if not new_collab:
            click.echo(click.style("Un collaborateur avec cet email existe déjà.", fg="red"))
            return
        
        click.echo(click.style(f"Collaborateur {name} ajouté avec succès !", fg="green"))

@collaborators.command()
@click.argument("collab_id", type=int)
def update(collab_id):
    valid_user = verify_token(get_token())
    if not valid_user:
        click.echo(click.style("Vous devez être connecté.", fg="red"))
        return

    click.echo("Laissez vide pour ne pas modifier")
    name = click.prompt("Nouveau nom", default="")
    email = click.prompt("Nouvel email", default="")
    password = click.prompt("Nouveau mot de passe", default="", hide_input=True)
    
    kwargs = {}
    if name:
        kwargs["name"] = name
    if email:
        kwargs["email"] = email
    if password:
        kwargs["password"] = password
    
    with Session() as session:
        service = CollaboratorsService(session)
        collab = service.update_collaborator(collab_id, **kwargs)
        if not collab:
            click.echo(click.style("Collaborateur non trouvé.", fg="red"))
            return
        
        click.echo(click.style(f"Collaborateur {collab.name} mis à jour avec succès !", fg="green"))

@collaborators.command()
@click.argument("collab_id", type=int)
def delete(collab_id):
    valid_user = verify_token(get_token())
    if not valid_user:
        click.echo(click.style("Vous devez être connecté.", fg="red"))
        return
    
    with Session() as session:
        service = CollaboratorsService(session)
        success = service.delete_collaborator(collab_id)
        if not success:
            click.echo(click.style("Collaborateur non trouvé.", fg="red"))
            return
        
        click.echo(click.style("Collaborateur supprimé avec succès !", fg="green"))