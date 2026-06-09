import click
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required, roles_required
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
@login_required
def delete():
    client_id = click.prompt("N° du client", type=int)
    with Session() as session:
        service = ClientsService(session)
        success = service.delete_client(client_id)
        if success:
            click.echo(click.style("Client supprimé avec succès !", fg="green"))
        else:
            click.echo(click.style("Client non trouvé.", fg="red"))

@clients.command()
@login_required
@roles_required("commercial")
def update():
    email_search = click.prompt("Email du client à modifier")
    click.echo("Laissez vide pour ne pas modifier")
    first_name = click.prompt("Nouveau prénom", default="")
    last_name = click.prompt("Nouveau nom", default="")
    new_email = click.prompt("Nouvel email", default="")
    phone_number = click.prompt("Nouveau téléphone", default="")
    company = click.prompt("Nouvelle société", default="")

    kwargs = {}
    if first_name: kwargs["first_name"] = first_name
    if last_name: kwargs["last_name"] = last_name
    if new_email: kwargs["email"] = new_email
    if phone_number: kwargs["phone_number"] = phone_number
    if company: kwargs["company"] = company

    payload = verify_token(get_token())
    collaborator_id = payload["id"]

    with Session() as session:
        service = ClientsService(session)
        client = service.update_client(email_search, collaborator_id, **kwargs)
        if not client:
            click.echo(click.style("Client non trouvé ou accès refusé.", fg="red"))
            return
        click.echo(click.style("Client mis à jour !", fg="green"))

# @clients.command()
# @login_required
# @roles_required("commercial")
# def delete():
#     email_search = click.prompt("Email du client à supprimer")
#     payload = verify_token(get_token())
#     collaborator_id = payload["id"]
#     with Session() as session:
#         service = ClientsService(session)
#         success = service.delete_client(email_search, collaborator_id)
#         if success:
#             click.echo(click.style("Client supprimé !", fg="green"))
#         else:
#             click.echo(click.style("Client non trouvé ou accès refusé.", fg="red"))