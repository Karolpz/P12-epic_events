from epicevent.models import Contract, Client
from sqlalchemy.orm import Session

class ContractsService:
    """Service de gestion des contrats."""

    def __init__(self, session: Session):
        """Initialise le service avec une session SQLAlchemy."""
        self.session = session

    def list_contracts(self):
        """Retourne la liste de tous les contrats."""
        return self.session.query(Contract).all()

    def add_contract(self, client_email, collaborator_id, amount):
        """Crée un contrat non signé pour un client existant. Retourne None si le client est introuvable."""
        client = self.session.query(Client).filter(Client.email == client_email).first()

        if not client:
            return None

        new_contract = Contract(
            client_id=client.id,
            collaborator_id=collaborator_id,
            amount=amount,
            amount_to_pay=amount,
            is_signed=False
        )
        self.session.add(new_contract)
        self.session.commit()
        return new_contract

    def update_contract(self, contract_id, **kwargs):
        """Met à jour les champs d'un contrat. Retourne None si le contrat est introuvable.

        Les champs `amount` et `amount_to_pay` sont traités séparément via les méthodes du modèle.
        """
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            return None
        if "amount" in kwargs:
            contract.amount = kwargs.pop("amount")
        if "amount_to_pay" in kwargs:
            contract.update_amount(kwargs.pop("amount_to_pay"))
        for key, value in kwargs.items():
            setattr(contract, key, value)
        self.session.commit()
        return contract

    def sign_contract(self, contract_id):
        """Signe un contrat existant. Retourne None si le contrat est introuvable."""
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            return None
        contract.sign()
        self.session.commit()
        return contract

    def delete_contract(self, contract_id):
        """Supprime un contrat par son identifiant. Retourne False si introuvable."""
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            return False
        self.session.delete(contract)
        self.session.commit()
        return True