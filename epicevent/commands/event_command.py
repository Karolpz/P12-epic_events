import click
from epicevent.models.base import Session
from epicevent.utils.decorators import login_required, roles_required
from epicevent.utils.token import get_token, verify_token
from epicevent.services.events_service import EventsService
from epicevent.models import Contract

@click.group()
def events():
    pass

@events.command()
@login_required
def list():
    with Session() as session:
        service = EventsService(session)
        events = service.list_events()
        if not events:
            click.echo(click.style("Aucun événement trouvé.", fg="yellow"))
            return
        
        click.echo(click.style("Liste des événements :", fg="green"))
        for event in events:
            click.echo(f"- Événement n° : {event.id}, Titre: {event.title}, Lieu: {event.location}")

@events.command()
@login_required
@roles_required("commercial")
def add():
    contract_id = click.prompt("N° du contrat associé", type=int)
    
    with Session() as session:
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            click.echo(click.style("Contrat introuvable.", fg="red"))
            return
        if not contract.is_signed:
            click.echo(click.style("Le contrat n'est pas signé.", fg="red"))
            return
    
    title = click.prompt("Titre de l'événement")
    location = click.prompt("Lieu de l'événement")
    start_date = click.prompt("Date de début (YYYY-MM-DD HH:MM)")
    end_date = click.prompt("Date de fin (YYYY-MM-DD HH:MM)")
    
    valid_user = verify_token(get_token())
    collaborator_id = valid_user["id"]

    with Session() as session:
        service = EventsService(session)
        event = service.add_event(collaborator_id, title, start_date, end_date, location, contract_id)
        if event:
            click.echo(click.style(f"Événement ajouté n° : {event.id}", fg="green"))
        else:
            click.echo(click.style("Erreur lors de l'ajout.", fg="red"))

@events.command()
@login_required
@roles_required("support")
def update():
    event_id = click.prompt("N° de l'événement", type=int)
    click.echo("Laissez vide pour ne pas modifier")
    title = click.prompt("Nouveau titre", default="")
    location = click.prompt("Nouveau lieu", default="")
    start_date = click.prompt("Nouvelle date de début", default="")
    end_date = click.prompt("Nouvelle date de fin", default="")
    notes = click.prompt("Notes", default="")

    kwargs = {}
    if title: kwargs["title"] = title
    if location: kwargs["location"] = location
    if start_date: kwargs["start_date"] = start_date
    if end_date: kwargs["end_date"] = end_date
    if notes: kwargs["notes"] = notes

    payload = verify_token(get_token())
    collaborator_id = payload["id"]

    with Session() as session:
        service = EventsService(session)
        event = service.update_event(event_id, collaborator_id, **kwargs)
        if not event:
            click.echo(click.style("Événement non trouvé ou accès refusé.", fg="red"))
            return
        click.echo(click.style(f"Événement mis à jour !", fg="green"))

@events.command()
@login_required
@roles_required("gestion")
def assign():
    event_id = click.prompt("N° de l'événement", type=int)
    collaborator_id = click.prompt("N° du collaborateur à assigner", type=int)
    
    with Session() as session:
        service = EventsService(session)
        event = service.assign_support(event_id, collaborator_id)
        if event:
            click.echo(click.style(f"Support assigné à l'événement n° : {event.id}", fg="green"))
        else:
            click.echo(click.style("Erreur lors de l'assignation du support. Vérifiez que l'événement et le collaborateur existent.", fg="red"))