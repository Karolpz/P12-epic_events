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

    def add_event(self, collaborator_id, title, start_date, end_date, location, contract_id):
        """Crée un événement lié à un contrat signé. Retourne None si le contrat est introuvable ou non signé."""
        contract = self.session.query(Contract).filter_by(id=contract_id).first()

        if not contract:
            return None
        if not contract.is_signed:
            return None

        new_event = Event(
            title=title,
            location=location,
            start_date=start_date,
            end_date=end_date,
            participants_number=0,
            contract_id=contract_id,
            notes="",
            collaborator_id=collaborator_id
        )
        self.session.add(new_event)
        self.session.commit()
        return new_event

    def update_event(self, event_id, **kwargs):
        """Met à jour les champs d'un événement. Retourne None si l'événement est introuvable."""
        event = self.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return None
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