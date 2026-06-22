from epicevent.models import Event, Contract, Collaborator
from sqlalchemy.orm import Session

class EventsService:
    """Service de gestion des événements."""

    def __init__(self, session: Session):
        """Initialise le service avec une session SQLAlchemy."""
        self.session = session

    def list_events(self):
        """Retourne la liste de tous les événements."""
        return self.session.query(Event).all()

    def add_event(self, commercial_id, title, start_date, end_date, location, contract_id):
        """Crée un événement lié à un contrat signé. Retourne None si le contrat est introuvable ou non signé."""
        contract = self.session.query(Contract).filter_by(id=contract_id).first()

        if not contract:
            return None

        new_event = Event(
            title=title,
            location=location,
            start_date=start_date,
            end_date=end_date,
            participants_number=0,
            contract_id=contract_id,
            notes="",
            commercial_id=commercial_id,
            support_id=None
        )
        new_event.set_dates(start_date, end_date)
        self.session.add(new_event)
        self.session.commit()
        return new_event

    def update_event(self, event_id, **kwargs):
        event = self.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return None
        if "start_date" in kwargs or "end_date" in kwargs:
            start = kwargs.pop("start_date", event.start_date)
            end = kwargs.pop("end_date", event.end_date)
            event.set_dates(start, end)
        for key, value in kwargs.items():
            setattr(event, key, value)
        self.session.commit()
        return event

    def assign_support(self, event_id, collaborator_id):
        """Assigne un collaborateur support à un événement. Retourne None si l'événement ou le collaborateur est introuvable."""
        collaborator = self.session.query(Collaborator).filter_by(id=collaborator_id).first()
        if not collaborator:
            return None
        event = self.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return None
        event.assign_support(collaborator)
        self.session.commit()
        return event