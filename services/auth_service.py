from models import Collaborator
from utils.token import generate_token, verify_token, get_token, delete_token

class AuthService:
    def __init__(self, session):
        self.session = session

    def login(self, email, password):
        collaborator = self.session.query(Collaborator).filter(Collaborator.email == email).first()

        if not collaborator:
            return None
        
        if collaborator.verify_password(password):
            collaborator.token = generate_token(collaborator)
            return collaborator

        return None

    def register(self, name, email, password, role):
        collaborator = Collaborator(name=name, email=email, role=role)
        collaborator.set_password(password)
        self.session.add(collaborator)
        self.session.commit()
        return collaborator
    
    def logout(self):
        return delete_token()