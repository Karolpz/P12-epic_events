import click
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required
from epicevent.services.clients_service import ClientsService
from epicevent.utils.token import get_token, verify_token

@click.group()
def clients():
    pass

@clients.command()
@login_required
def list():
    with Session() as session:
        service = ClientsService(session)
        clients = service.list_clients()
        if not clients:
            click.echo(click.style("Aucun client trouvé.", fg="yellow"))
            return
        
        click.echo(click.style("Liste des clients :", fg="green"))
        for client in clients:
            click.echo(f"- {client.first_name} {client.last_name} ({client.email}) - Société: {client.company}")

@clients.command()
@click.argument("client_id", type=int)
@login_required
def delete(client_id):
    with Session() as session:
        service = ClientsService(session)
        success = service.delete_client(client_id)
        if success:
            click.echo(click.style("Client supprimé avec succès !", fg="green"))
        else:
            click.echo(click.style("Client non trouvé.", fg="red"))

@clients.command()
@click.argument("client_id", type=int)
@login_required
def update(client_id):
    click.echo("Laissez vide pour ne pas modifier")
    first_name = click.prompt("Nouveau prénom", default="")
    last_name = click.prompt("Nouveau nom", default="")
    email = click.prompt("Nouvel email", default="")
    phone_number = click.prompt("Nouveau téléphone", default="")
    company = click.prompt("Nouvelle société", default="")

    kwargs = {}
    if first_name: kwargs["first_name"] = first_name
    if last_name: kwargs["last_name"] = last_name
    if email: kwargs["email"] = email
    if phone_number: kwargs["phone_number"] = phone_number
    if company: kwargs["company"] = company

    with Session() as session:
        service = ClientsService(session)
        client = service.update_client(client_id, **kwargs)
        if not client:
            click.echo(click.style("Client non trouvé.", fg="red"))
            return
        click.echo(click.style("Client mis à jour !", fg="green"))

@clients.command()
@login_required
def add():
    first_name = click.prompt("Prénom du client")
    last_name = click.prompt("Nom du client")
    email = click.prompt("Email du client")
    phone_number = click.prompt("Numéro de téléphone du client")
    company = click.prompt("Société du client")
    valid_user = verify_token(get_token())
    collaborator_id = valid_user["id"]

    with Session() as session:
        service = ClientsService(session)
        new_client = service.add_client(first_name, last_name, email, phone_number, company, collaborator_id)
        if not new_client:
            click.echo(click.style("Un client avec cet email existe déjà.", fg="red"))
            return
        
        click.echo(click.style(f"Client {first_name} {last_name} ajouté avec succès !", fg="green"))