import pytest
from epicevent.models import Client
from epicevent.services.clients_service import ClientsService


@pytest.fixture
def service(session):
    return ClientsService(session)


class TestAddClient:
    def test_add_returns_client(self, service, commercial_user):
        result = service.add_client(
            first_name="Marie",
            last_name="Dupont",
            email="marie@corp.com",
            phone_number="0611111111",
            company="Corp",
            collaborator_id=commercial_user.id,
        )
        assert result is not None
        assert result.email == "marie@corp.com"
        assert result.collaborator_id == commercial_user.id

    def test_add_duplicate_email_returns_none(self, service, commercial_user):
        service.add_client("A", "B", "dup@corp.com", "0600000000", "Corp", commercial_user.id)
        result = service.add_client("C", "D", "dup@corp.com", "0600000001", "Corp", commercial_user.id)
        assert result is None

    def test_add_persists_to_db(self, service, session, commercial_user):
        service.add_client("Luc", "Blanc", "luc@corp.com", None, "Corp", commercial_user.id)
        found = session.query(Client).filter_by(email="luc@corp.com").first()
        assert found is not None


class TestUpdateClient:
    def test_owner_can_update(self, service, sample_client, commercial_user):
        result = service.update_client(
            sample_client.email, commercial_user.id, company="New Corp"
        )
        assert result is not None
        assert result.company == "New Corp"

    def test_non_owner_cannot_update(self, service, sample_client, other_commercial):
        result = service.update_client(
            sample_client.email, other_commercial.id, company="Hacked Corp"
        )
        assert result is None

    def test_update_unknown_email_returns_none(self, service, commercial_user):
        result = service.update_client("ghost@corp.com", commercial_user.id, company="X")
        assert result is None

    def test_update_phone_number(self, service, sample_client, commercial_user):
        result = service.update_client(
            sample_client.email, commercial_user.id, phone_number="0699999999"
        )
        assert result.phone_number == "0699999999"


class TestDeleteClient:
    def test_owner_can_delete(self, service, sample_client, commercial_user):
        result = service.delete_client(sample_client.email, commercial_user.id)
        assert result is True

    def test_delete_removes_from_db(self, service, session, sample_client, commercial_user):
        email = sample_client.email
        service.delete_client(email, commercial_user.id)
        assert session.query(Client).filter_by(email=email).first() is None

    def test_non_owner_cannot_delete(self, service, sample_client, other_commercial):
        result = service.delete_client(sample_client.email, other_commercial.id)
        assert result is False
