import click
from datetime import datetime
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required, roles_required
from epicevent.utils.token import get_token, verify_token
from epicevent.services.events_service import EventsService
from epicevent.services.contracts_service import ContractsService
from epicevent.services.collaborators_service import CollaboratorsService


DATE_FORMAT = "%Y-%m-%d %H:%M"


@click.group()
def events():
    pass


@events.command()
@login_required
def list():
    with Session() as session:
        service = EventsService(session)
        event_list = service.list_events()
        if not event_list:
            click.echo(click.style("Aucun événement trouvé.", fg="yellow"))
            return

        click.echo(click.style("Liste des événements :", fg="green"))
        for event in event_list:
            click.echo(f"- Événement n° : {event.id}, Titre: {event.title}, Lieu: {event.location}, Support: {event.support.name if event.support else 'Non assigné'}")


@events.command()
@login_required
@roles_required("commercial")
def add():
    contract_id = click.prompt("N° du contrat associé", type=int)

    valid_user = verify_token(get_token())
    commercial_id = valid_user["id"]

    with Session() as session:
        service = ContractsService(session)
        contract = service.get_contract_by_id(contract_id)
        if not contract or not contract.is_signed:
            click.echo(click.style("Contrat introuvable ou non signé.", fg="red"))
            return

        title = click.prompt("Titre de l'événement")
        location = click.prompt("Lieu de l'événement")
        start_date_str = click.prompt("Date de début (YYYY-MM-DD HH:MM)")
        end_date_str = click.prompt("Date de fin (YYYY-MM-DD HH:MM)")

        try:
            start_date = datetime.strptime(start_date_str, DATE_FORMAT)
            end_date = datetime.strptime(end_date_str, DATE_FORMAT)
        except ValueError:
            click.echo(click.style("Format de date invalide. Utilisez YYYY-MM-DD HH:MM", fg="red"))
            return

        service = EventsService(session)
        event = service.add_event(commercial_id, title, start_date, end_date, location, contract_id)
        if event:
            click.echo(click.style(f"Événement ajouté n° : {event.id}", fg="green"))
        else:
            click.echo(click.style("Contrat introuvable ou non signé.", fg="red"))

@events.command()
@login_required
@roles_required("support")
def update():
    event_id = click.prompt("N° de l'événement", type=int)

    payload = verify_token(get_token())
    support_id = payload["id"]

    with Session() as session:
        collaborator_service = CollaboratorsService(session)
        support = collaborator_service.get_collaborator_by_id(support_id)
        event_service = EventsService(session)
        event = event_service.get_event_by_id(event_id)
        if not event or not event.can_edit(support):
            click.echo(click.style("Événement non trouvé ou accès refusé.", fg="red"))
            return

        click.echo("Laissez vide pour ne pas modifier")
        title = click.prompt("Nouveau titre", default="")
        location = click.prompt("Nouveau lieu", default="")
        start_date_str = click.prompt("Nouvelle date de début (YYYY-MM-DD HH:MM)", default="")
        end_date_str = click.prompt("Nouvelle date de fin (YYYY-MM-DD HH:MM)", default="")
        notes = click.prompt("Notes", default="")

        kwargs = {}
        if title: 
            kwargs["title"] = title
        if location: 
            kwargs["location"] = location
        if start_date_str:
            try:
                kwargs["start_date"] = datetime.strptime(start_date_str, DATE_FORMAT)
            except ValueError:
                click.echo(click.style("Format de date de début invalide.", fg="red"))
                return
        if end_date_str:
            try:
                kwargs["end_date"] = datetime.strptime(end_date_str, DATE_FORMAT)
            except ValueError:
                click.echo(click.style("Format de date de fin invalide.", fg="red"))
                return
        if notes: 
            kwargs["notes"] = notes

        event_service.update_event(event_id, **kwargs)
        click.echo(click.style("Événement mis à jour !", fg="green"))


@events.command()
@login_required
@roles_required("gestion")
def assign():
    event_id = click.prompt("N° de l'événement", type=int)
    collaborator_email = click.prompt("Email du collaborateur à assigner", type=str)

    with Session() as session:
        service = EventsService(session)
        event = service.assign_support(event_id, collaborator_email)
        if event:
            click.echo(click.style(f"Support assigné à l'événement n° : {event.id}", fg="green"))
        else:
            click.echo(click.style("Événement ou collaborateur introuvable.", fg="red"))
