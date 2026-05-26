from epicevent.models import Collaborator
from epicevent.utils.token import generate_token, verify_token, get_token, delete_token
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, session : Session):
        self.session = session

    def login(self, email, password):
        collaborator = self.session.query(Collaborator).filter(Collaborator.email == email).first()

        if not collaborator:
            return None
        
        if collaborator.verify_password(password):
            generate_token(collaborator)
            return collaborator

        return None

    def logout(self):
        return delete_token()