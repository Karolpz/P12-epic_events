import click
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required, roles_required
from epicevent.services.clients_service import ClientsService
from epicevent.utils.token import get_token, verify_token
from epicevent.models.collaborators import Collaborator
from epicevent.models.clients import Client
@click.group()
def clients():
    pass


@clients.command()
@login_required
def list():
    with Session() as session:
        service = ClientsService(session)
        client_list = service.list_clients()
        if not client_list:
            click.echo(click.style("Aucun client trouvé.", fg="yellow"))
            return

        click.echo(click.style("Liste des clients :", fg="green"))
        for client in client_list:
            click.echo(f"- {client.first_name} {client.last_name} ({client.email}) - Société: {client.company}")


@clients.command()
@login_required
@roles_required("commercial")
def add():
    first_name = click.prompt("Prénom du client")
    last_name = click.prompt("Nom du client")
    email = click.prompt("Email du client")
    phone_number = click.prompt("Téléphone", default="")
    company = click.prompt("Société")

    payload = verify_token(get_token())
    collaborator_id = payload["id"]

    with Session() as session:
        service = ClientsService(session)
        client = service.add_client(
            first_name, last_name, email, phone_number or None, company, collaborator_id
        )
        if not client:
            click.echo(click.style("Un client avec cet email existe déjà.", fg="red"))
            return
        click.echo(click.style(f"Client {first_name} {last_name} ajouté avec succès !", fg="green"))


@clients.command()
@login_required
@roles_required("commercial")
def update():
    email_search = click.prompt("Email du client à modifier")

    payload = verify_token(get_token())
    collaborator_id = payload["id"]

    with Session() as session:
        collaborator = session.get(Collaborator, collaborator_id)
        client = session.query(Client).filter_by(email=email_search).first()
        if not client or not client.can_edit(collaborator):
            click.echo(click.style("Client non trouvé ou accès refusé.", fg="red"))
            return

        click.echo("Laissez vide pour ne pas modifier")
        first_name = click.prompt("Nouveau prénom", default="")
        last_name = click.prompt("Nouveau nom", default="")
        new_email = click.prompt("Nouvel email", default="")
        phone_number = click.prompt("Nouveau téléphone", default="")
        company = click.prompt("Nouvelle société", default="")

        kwargs = {}
        if first_name: 
            kwargs["first_name"] = first_name
        if last_name: 
            kwargs["last_name"] = last_name
        if new_email: 
            kwargs["email"] = new_email
        if phone_number: 
            kwargs["phone_number"] = phone_number
        if company: 
            kwargs["company"] = company

        service = ClientsService(session)
        service.update_client(email_search, **kwargs)
        click.echo(click.style("Client mis à jour !", fg="green"))