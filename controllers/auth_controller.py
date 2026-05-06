from models import Collaborator
from argon2 import PasswordHasher

ph = PasswordHasher()

class AuthController:
    def __init__(self, session):
        self.session = session

    def login(self, email, password):
        collaborator = self.session.query(Collaborator).filter(Collaborator.email == email).first()

        if not collaborator:
            return None
        
        try:
            ph.verify(collaborator.password, password)
            return collaborator
        except:
            return None

    def register(self, name, email, password, role):
        hashed_password = ph.hash(password)
        new_collaborator = Collaborator(name=name, email=email, password=hashed_password, role=role)
        self.session.add(new_collaborator)
        self.session.commit()
        return new_collaborator
    
    def logout(self):
        pass