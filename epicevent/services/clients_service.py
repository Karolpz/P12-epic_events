from epicevent.models import Client
from sqlalchemy.orm import Session

class ClientsService:
    def __init__(self, session: Session):
        self.session = session

    def list_clients(self):
        return self.session.query(Client).all()
    
    def add_client(self, first_name, last_name, email, phone_number, company, collaborator_id):
        if self.session.query(Client).filter(Client.email == email).first():
            return None
        
        new_client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            company=company,
            collaborator_id=collaborator_id
        )
        self.session.add(new_client)
        self.session.commit()
        return new_client
    
    def update_client(self, client_id, **kwargs):
        client = self.session.query(Client).filter(Client.id == client_id).first()
        if not client:
            return None
        
        for key, value in kwargs.items():
            setattr(client, key, value)
        
        self.session.commit()
        return client

    def delete_client(self, client_id):
        client = self.session.query(Client).filter(Client.id == client_id).first()
        if not client:
            return False
        
        self.session.delete(client)
        self.session.commit()
        return True