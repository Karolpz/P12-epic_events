from epicevent.models import Contract
from sqlalchemy.orm import Session
from epicevent.services.clients_service import ClientsService

class ContractsService:
    """Service de gestion des contrats."""

    def __init__(self, session: Session):
        """Initialise le service avec une session SQLAlchemy et le service des clients."""
        self.session = session
        self.clients_service = ClientsService(session)

    def list_contracts(self):
        """Retourne la liste de tous les contrats."""
        return self.session.query(Contract).all()
    
    def get_contract_by_id(self, contract_id):
        """Retourne un contrat par son ID. Retourne None si le contrat n'existe pas."""
        return self.session.query(Contract).filter_by(id=contract_id).first()
    
    def list_unsigned_contracts(self):
        """Retourne la liste des contrats non signés."""
        return self.session.query(Contract).filter_by(is_signed=False).all()
    
    def list_unpaid_contracts(self):
        """Retourne la liste des contrats non payés."""
        return self.session.query(Contract).filter(Contract.amount_to_pay > 0).all()

    def add_contract(self, client_email, collaborator_id, amount):
        """Crée un contrat non signé pour un client existant. Retourne None si le client est introuvable."""
        client = self.clients_service.get_client_by_email(client_email)

        if not client:
            return None

        new_contract = Contract(
            client_id=client.id,
            collaborator_id=collaborator_id,
            is_signed=False
        )
        new_contract.set_amount(amount)
        self.session.add(new_contract)
        self.session.commit()
        return new_contract

    def update_contract(self, contract_id, **kwargs):
        """Met à jour les champs d'un contrat. Retourne None si le contrat est introuvable.

        Les champs `amount` et `amount_to_pay` sont traités séparément via les méthodes du modèle.
        """
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            return None
        if "amount" in kwargs:
            contract.total_amount(kwargs.pop("amount"))
        if "amount_to_pay" in kwargs:
            contract.update_amount(kwargs.pop("amount_to_pay"))
        for key, value in kwargs.items():
            setattr(contract, key, value)
        self.session.commit()
        return contract

    def sign_contract(self, contract_id):
        """Signe un contrat existant. Retourne None si le contrat est introuvable."""
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            return None
        contract.sign()
        self.session.commit()
        return contract