from epicevent.models import Collaborator
from epicevent.utils.token import generate_token, verify_token, get_token, delete_token
from sqlalchemy.orm import Session

class CollaboratorsService:
    def __init__(self, session : Session):
        self.session = session

    def list_collaborators(self):
        return self.session.query(Collaborator).all()

    def add_collaborator(self, employee_id, name, email, password, role):
        if self.session.query(Collaborator).filter(Collaborator.email == email).first():
            return None
        
        new_collab = Collaborator(employee_id=employee_id, name=name, email=email, role=role)
        new_collab.set_password(password)
        self.session.add(new_collab)
        self.session.commit()
        return new_collab