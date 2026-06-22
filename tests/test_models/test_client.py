import pytest
from epicevent.models import Client, Collaborator, RoleEnum


def _make_client(collaborator_id):
    return Client(
        first_name="Jean",
        last_name="Martin",
        email="jean@company.com",
        company="Company SA",
        collaborator_id=collaborator_id,
    )


def _make_collab(role, collab_id):
    collab = Collaborator(name="X", email="x@x.com", role=role)
    collab.id = collab_id
    return collab


class TestCanEdit:
    def test_owner_commercial_can_edit(self):
        client = _make_client(collaborator_id=3)
        commercial = _make_collab(RoleEnum.commercial, collab_id=3)
        assert client.can_edit(commercial) is True

    def test_non_owner_commercial_cannot_edit(self):
        client = _make_client(collaborator_id=3)
        other = _make_collab(RoleEnum.commercial, collab_id=7)
        assert client.can_edit(other) is False

    def test_gestion_without_ownership_cannot_edit(self):
        client = _make_client(collaborator_id=3)
        gestion = _make_collab(RoleEnum.gestion, collab_id=99)
        assert client.can_edit(gestion) is False

    def test_support_without_ownership_cannot_edit(self):
        client = _make_client(collaborator_id=3)
        support = _make_collab(RoleEnum.support, collab_id=10)
        assert client.can_edit(support) is False
