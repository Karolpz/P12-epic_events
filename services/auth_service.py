from models import Collaborator

class AuthService:
    def __init__(self, session):
        self.session = session

    def login(self, email, password):
        collaborator = self.session.query(Collaborator).filter(Collaborator.email == email).first()

        if not collaborator:
            return None
        
        if collaborator.verify_password(password):
            return collaborator

        return None

    def register(self, name, email, password, role):
        collaborator = Collaborator(name=name, email=email, role=role)
        collaborator.set_password(password)
        self.session.add(collaborator)
        self.session.commit()
        return collaborator
    
    def logout(self):
        pass