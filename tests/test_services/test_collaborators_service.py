import pytest
from epicevent.models import Collaborator, RoleEnum
from epicevent.services.collaborators_service import CollaboratorsService


@pytest.fixture
def service(session):
    return CollaboratorsService(session)


class TestAddCollaborator:
    def test_add_returns_collaborator(self, service):
        result = service.add_collaborator(
            name="New User", email="new@epic.io", password="Pass123!", role=RoleEnum.commercial
        )
        assert result is not None
        assert result.email == "new@epic.io"
        assert result.role == RoleEnum.commercial

    def test_add_hashes_password(self, service):
        result = service.add_collaborator(
            name="New User", email="new@epic.io", password="Pass123!", role=RoleEnum.commercial
        )
        assert result.password != "Pass123!"

    def test_add_duplicate_email_returns_none(self, service):
        service.add_collaborator(name="First", email="dup@epic.io", password="Pass!", role=RoleEnum.commercial)
        result = service.add_collaborator(name="Second", email="dup@epic.io", password="Pass!", role=RoleEnum.support)
        assert result is None

    def test_add_persists_to_db(self, service, session):
        service.add_collaborator(name="Persist", email="persist@epic.io", password="Pass!", role=RoleEnum.gestion)
        found = session.query(Collaborator).filter_by(email="persist@epic.io").first()
        assert found is not None


class TestUpdateCollaborator:
    def test_update_name(self, service, gestion_user):
        result = service.update_collaborator(gestion_user.email, name="Alice Updated")
        assert result is not None
        assert result.name == "Alice Updated"

    def test_update_password_is_hashed(self, service, gestion_user):
        result = service.update_collaborator(gestion_user.email, password="NewPass!")
        assert result is not None
        assert result.verify_password("NewPass!") is True

    def test_update_unknown_email_returns_none(self, service):
        result = service.update_collaborator("nobody@epic.io", name="Ghost")
        assert result is None

    def test_update_role(self, service, commercial_user):
        result = service.update_collaborator(commercial_user.email, role=RoleEnum.support)
        assert result.role == RoleEnum.support


class TestDeleteCollaborator:
    def test_delete_existing_returns_true(self, service, gestion_user):
        result = service.delete_collaborator(gestion_user.id)
        assert result is True

    def test_delete_removes_from_db(self, service, session, gestion_user):
        collab_id = gestion_user.id
        service.delete_collaborator(collab_id)
        assert session.query(Collaborator).filter_by(id=collab_id).first() is None

    def test_delete_unknown_id_returns_false(self, service):
        result = service.delete_collaborator(99999)
        assert result is False
