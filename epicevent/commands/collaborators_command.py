import click
from epicevent.models.base import Session
from epicevent.models.collaborators import Collaborator, RoleEnum
from epicevent.services.collaborators_service import CollaboratorsService
from epicevent.utils.decorators import login_required

@click.group()
def collaborators():
    pass

@collaborators.command()
@login_required
def list():
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
@login_required
def add():
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
@login_required
def update():
    click.echo("Laissez vide pour ne pas modifier")
    collab_id = click.prompt("N° du collaborateur", type=int)
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
@login_required
def delete():
    collab_id = click.prompt("N° du collaborateur", type=int)
    with Session() as session:
        service = CollaboratorsService(session)
        success = service.delete_collaborator(collab_id)
        if not success:
            click.echo(click.style("Collaborateur non trouvé.", fg="red"))
            return
        
        click.echo(click.style("Collaborateur supprimé avec succès !", fg="green"))