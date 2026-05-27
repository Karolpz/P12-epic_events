from epicevent.models import Collaborator
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
    
    def update_collaborator(self, collab_id, **kwargs):
        collab = self.session.query(Collaborator).filter(Collaborator.id == collab_id).first()
        if not collab:
            return None

        if 'password' in kwargs:
            collab.set_password(kwargs.pop('password'))
        
        for key, value in kwargs.items():
            setattr(collab, key, value)
        
        self.session.commit()
        return collab
    
    def delete_collaborator(self, collab_id):
        collab = self.session.query(Collaborator).filter(Collaborator.id == collab_id).first()
        if not collab:
            return False
        
        self.session.delete(collab)
        self.session.commit()
        return True