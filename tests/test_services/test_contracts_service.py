import pytest
from epicevent.models import Contract
from epicevent.services.contracts_service import ContractsService


@pytest.fixture
def service(session):
    return ContractsService(session)


class TestAddContract:
    def test_add_returns_contract(self, service, sample_client, commercial_user):
        result = service.add_contract(
            client_email=sample_client.email,
            collaborator_id=commercial_user.id,
            amount=3000.0,
        )
        assert result is not None
        assert result.amount == 3000.0
        assert result.amount_to_pay == 3000.0
        assert result.is_signed is False

    def test_add_unknown_client_returns_none(self, service, commercial_user):
        result = service.add_contract(
            client_email="ghost@corp.com",
            collaborator_id=commercial_user.id,
            amount=1000.0,
        )
        assert result is None

    def test_add_persists_to_db(self, service, session, sample_client, commercial_user):
        contract = service.add_contract(sample_client.email, commercial_user.id, 2000.0)
        found = session.query(Contract).filter_by(id=contract.id).first()
        assert found is not None


class TestSignContract:
    def test_sign_unsigned_contract(self, service, unsigned_contract):
        result = service.sign_contract(unsigned_contract.id)
        assert result is not None
        assert result.is_signed is True

    def test_sign_already_signed_raises(self, service, signed_contract):
        with pytest.raises(Exception, match="déjà signé"):
            service.sign_contract(signed_contract.id)

    def test_sign_unknown_id_returns_none(self, service):
        result = service.sign_contract(99999)
        assert result is None


class TestUpdateContract:
    def test_gestion_can_update_any_contract(self, service, unsigned_contract, gestion_user):
        result = service.update_contract(
            unsigned_contract.id, gestion_user.id, amount_to_pay=2000.0
        )
        assert result is not None
        assert result.amount_to_pay == 2000.0

    def test_commercial_owner_can_update(self, service, unsigned_contract, commercial_user):
        result = service.update_contract(
            unsigned_contract.id, commercial_user.id, amount_to_pay=1500.0
        )
        assert result is not None
        assert result.amount_to_pay == 1500.0

    def test_non_owner_cannot_update(self, service, unsigned_contract, other_commercial):
        result = service.update_contract(
            unsigned_contract.id, other_commercial.id, amount_to_pay=0.0
        )
        assert result is None

    def test_update_unknown_contract_returns_none(self, service, gestion_user):
        result = service.update_contract(99999, gestion_user.id, amount_to_pay=100.0)
        assert result is None
