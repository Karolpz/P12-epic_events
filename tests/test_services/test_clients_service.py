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
    def test_update_company(self, service, sample_client):
        result = service.update_client(sample_client.email, company="New Corp")
        assert result is not None
        assert result.company == "New Corp"

    def test_update_unknown_email_returns_none(self, service):
        result = service.update_client("ghost@corp.com", company="X")
        assert result is None

    def test_update_phone_number(self, service, sample_client):
        result = service.update_client(sample_client.email, phone_number="0699999999")
        assert result.phone_number == "0699999999"

    def test_update_multiple_fields(self, service, sample_client):
        result = service.update_client(
            sample_client.email, first_name="Nouveau", last_name="Nom"
        )
        assert result.first_name == "Nouveau"
        assert result.last_name == "Nom"

