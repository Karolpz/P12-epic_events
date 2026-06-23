from epicevent.models import Event, RoleEnum
from sqlalchemy.orm import Session
from epicevent.services.collaborators_service import CollaboratorsService
from epicevent.services.contracts_service import ContractsService

class EventsService:
    """Service de gestion des événements."""

    def __init__(self, session: Session):
        """Initialise le service avec une session SQLAlchemy et les services associés."""
        self.session = session
        self.collaborators_service = CollaboratorsService(session)
        self.contracts_service = ContractsService(session)

    def list_events(self):
        """Retourne la liste de tous les événements."""
        return self.session.query(Event).all()
    
    def get_event_by_id(self, event_id):
        """Retourne un événement par son ID. Retourne None si l'événement n'existe pas."""
        return self.session.query(Event).filter_by(id=event_id).first()

    def add_event(self, commercial_id, title, start_date, end_date, location, contract_id):
        """Crée un événement lié à un contrat signé. Retourne None si le contrat est introuvable ou non signé."""
        contract = self.contracts_service.get_contract_by_id(contract_id)
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
            commercial_id=commercial_id,
            support_id=None
        )
        new_event.set_dates(start_date, end_date)
        self.session.add(new_event)
        self.session.commit()
        return new_event

    def update_event(self, event_id, **kwargs):
        event = self.get_event_by_id(event_id)
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

    def assign_support(self, event_id, collaborator_email):
        """Assigne un collaborateur support à un événement. Retourne None si l'événement ou le collaborateur est introuvable."""
        collaborator = self.collaborators_service.get_collaborator_by_email(collaborator_email)
        if not collaborator:
            return None
        if collaborator.role != RoleEnum.support:
            return None
        event = self.get_event_by_id(event_id)
        if not event:
            return None
        event.assign_support(collaborator)
        self.session.commit()
        return event