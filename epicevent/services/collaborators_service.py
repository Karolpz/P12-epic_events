from epicevent.models import Collaborator
from sqlalchemy.orm import Session

class CollaboratorsService:
    """Service de gestion des collaborateurs."""

    def __init__(self, session: Session):
        """Initialise le service avec une session SQLAlchemy."""
        self.session = session

    def list_collaborators(self):
        """Retourne la liste de tous les collaborateurs."""
        return self.session.query(Collaborator).all()

    def add_collaborator(self, name, email, password, role):
        """Crée un nouveau collaborateur. Retourne None si l'email est déjà utilisé."""
        if self.session.query(Collaborator).filter(Collaborator.email == email).first():
            return None

        new_collab = Collaborator(name=name, email=email, role=role)
        new_collab.set_password(password)
        self.session.add(new_collab)
        self.session.commit()
        return new_collab

    def update_collaborator(self, email_id, **kwargs):
        """Met à jour les champs d'un collaborateur identifié par son email.

        Le mot de passe, s'il est fourni, est haché avant d'être enregistré.
        Retourne None si le collaborateur est introuvable.
        """
        collab = self.session.query(Collaborator).filter(Collaborator.email == email_id).first()
        if not collab:
            return None

        if 'password' in kwargs:
            collab.set_password(kwargs.pop('password'))

        for key, value in kwargs.items():
            setattr(collab, key, value)

        self.session.commit()
        return collab

    def delete_collaborator(self, collab_id):
        """Supprime un collaborateur par son identifiant. Retourne False si introuvable."""
        collab = self.session.query(Collaborator).filter(Collaborator.id == collab_id).first()
        if not collab:
            return False

        self.session.delete(collab)
        self.session.commit()
        return True