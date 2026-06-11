import pytest
from datetime import datetime
from epicevent.models import Event, Collaborator, RoleEnum


def _make_event(collaborator_id):
    return Event(
        title="Gala",
        location="Paris",
        start_date=datetime(2025, 6, 1),
        end_date=datetime(2025, 6, 2),
        participants_number=50,
        collaborator_id=collaborator_id,
    )


def _make_collab(role, collab_id):
    collab = Collaborator(name="X", email="x@x.com", role=role)
    collab.id = collab_id
    return collab


class TestCanEdit:
    def test_assigned_support_can_edit(self):
        event = _make_event(collaborator_id=4)
        support = _make_collab(RoleEnum.support, collab_id=4)
        assert event.can_edit(support) is True

    def test_non_assigned_support_cannot_edit(self):
        event = _make_event(collaborator_id=4)
        other_support = _make_collab(RoleEnum.support, collab_id=9)
        assert event.can_edit(other_support) is False

    def test_gestion_without_assignment_cannot_edit(self):
        # can_edit checks only collaborator_id equality, no role privilege
        event = _make_event(collaborator_id=4)
        gestion = _make_collab(RoleEnum.gestion, collab_id=99)
        assert event.can_edit(gestion) is False

    def test_commercial_without_assignment_cannot_edit(self):
        event = _make_event(collaborator_id=4)
        commercial = _make_collab(RoleEnum.commercial, collab_id=7)
        assert event.can_edit(commercial) is False


class TestAssignSupport:
    def test_assign_support_updates_collaborator_id(self):
        event = _make_event(collaborator_id=1)
        new_support = _make_collab(RoleEnum.support, collab_id=5)
        event.assign_support(new_support)
        assert event.collaborator_id == 5

    def test_assign_support_replaces_previous_assignment(self):
        event = _make_event(collaborator_id=3)
        first_support = _make_collab(RoleEnum.support, collab_id=3)
        second_support = _make_collab(RoleEnum.support, collab_id=8)
        event.assign_support(first_support)
        event.assign_support(second_support)
        assert event.collaborator_id == 8

    def test_can_edit_returns_true_after_assignment(self):
        event = _make_event(collaborator_id=1)
        support = _make_collab(RoleEnum.support, collab_id=5)
        event.assign_support(support)
        assert event.can_edit(support) is True
