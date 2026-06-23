from epicevent.models import Client
from sqlalchemy.orm import Session

class ClientsService:
    """Service de gestion des clients."""

    def __init__(self, session: Session):
        """Initialise le service avec une session SQLAlchemy."""
        self.session = session

    def list_clients(self):
        """Retourne la liste de tous les clients."""
        return self.session.query(Client).all()
    
    def get_client_by_email(self, email):
        """Retourne un client par son email. Retourne None si le client n'existe pas."""
        return self.session.query(Client).filter_by(email=email).first()

    def get_client_by_id(self, client_id):
        """Retourne un client par son ID. Retourne None si le client n'existe pas."""
        return self.session.query(Client).filter_by(id=client_id).first()

    def add_client(self, first_name, last_name, email, phone_number, company, collaborator_id):
        """Crée un nouveau client. Retourne None si l'email est déjà utilisé."""
        if self.get_client_by_email(email):
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

    def update_client(self, email, **kwargs):
        """Met à jour les champs d'un client identifié par son email. Retourne None si introuvable."""
        client = self.get_client_by_email(email)
        if not client:
            return None
        for key, value in kwargs.items():
            setattr(client, key, value)
        self.session.commit()
        return client

