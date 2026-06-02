from epicevent.models import Event, Contract, Collaborator
from sqlalchemy.orm import Session

class EventsService:
    def __init__(self, session: Session):
        self.session = session

    def list_events(self):
        return self.session.query(Event).all()
    
    def add_event(self, collaborator_id, title, start_date, end_date, location, contract_id):
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
    
        if not contract:
            return None
        if not contract.is_signed:
            return None
        
        new_event = Event(
            title = title,
            location = location,
            start_date = start_date,
            end_date = end_date,
            participants_number = 0,
            contract_id = contract_id,
            notes = "",
            collaborator_id = collaborator_id
        )
        self.session.add(new_event)
        self.session.commit()
        return new_event
    
    def update_event(self, event_id, collaborator_id, **kwargs):
        event = self.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return None
        if event.collaborator_id != collaborator_id:
            return None
        for key, value in kwargs.items():
            setattr(event, key, value)
        self.session.commit()
        return event
    
    def assign_support(self, event_id, collaborator_id):
        collaborator = self.session.query(Collaborator).filter_by(id=collaborator_id).first()
        event = self.session.query(Event).filter_by(id=event_id).first()
        if not event:
            return None
        event.assign_support(collaborator)
        self.session.commit()
        return event