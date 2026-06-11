from epicevent.models import Contract, Collaborator, Client
from sqlalchemy.orm import Session

class ContractsService:
    def __init__(self, session: Session):
        self.session = session

    def list_contracts(self):
        return self.session.query(Contract).all()

    def add_contract(self, client_email, collaborator_id, amount):

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

    def update_contract(self, contract_id, collaborator_id, **kwargs):
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            return None
        collaborator = self.session.get(Collaborator, collaborator_id)
        if not contract.can_edit(collaborator):
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
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            return None
        contract.sign()
        self.session.commit()
        return contract

    def delete_contract(self, contract_id):
        contract = self.session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            return False
        self.session.delete(contract)
        self.session.commit()
        return True