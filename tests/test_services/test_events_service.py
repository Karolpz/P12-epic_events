import pytest
from datetime import datetime
from epicevent.models import Event
from epicevent.services.events_service import EventsService


@pytest.fixture
def service(session):
    return EventsService(session)


START = datetime(2025, 10, 1, 9, 0)
END = datetime(2025, 10, 1, 18, 0)


class TestAddEvent:
    def test_add_on_signed_contract_returns_event(self, service, signed_contract, commercial_user):
        result = service.add_event(
            commercial_id=commercial_user.id,
            title="Conférence",
            start_date=START,
            end_date=END,
            location="Lyon",
            contract_id=signed_contract.id,
        )
        assert result is not None
        assert result.title == "Conférence"
        assert result.contract_id == signed_contract.id

    def test_add_on_unsigned_contract_returns_none(self, service, unsigned_contract, commercial_user):
        result = service.add_event(
            commercial_id=commercial_user.id,
            title="Conférence",
            start_date=START,
            end_date=END,
            location="Lyon",
            contract_id=unsigned_contract.id,
        )
        assert result is None

    def test_add_unknown_contract_returns_none(self, service, commercial_user):
        result = service.add_event(
            commercial_id=commercial_user.id,
            title="Ghost Event",
            start_date=START,
            end_date=END,
            location="Nowhere",
            contract_id=99999,
        )
        assert result is None

    def test_add_persists_to_db(self, service, session, signed_contract, commercial_user):
        event = service.add_event(
            commercial_user.id, "Test", START, END, "Paris", signed_contract.id
        )
        found = session.query(Event).filter_by(id=event.id).first()
        assert found is not None


class TestUpdateEvent:
    def test_update_location(self, service, sample_event):
        result = service.update_event(sample_event.id, location="Marseille")
        assert result is not None
        assert result.location == "Marseille"

    def test_update_participants_number(self, service, sample_event):
        result = service.update_event(sample_event.id, participants_number=200)
        assert result.participants_number == 200

    def test_update_notes(self, service, sample_event):
        result = service.update_event(sample_event.id, notes="Note mise à jour")
        assert result.notes == "Note mise à jour"

    def test_update_unknown_event_returns_none(self, service):
        result = service.update_event(99999, location="Nowhere")
        assert result is None

    def test_update_multiple_fields(self, service, sample_event):
        result = service.update_event(sample_event.id, location="Nice", participants_number=50)
        assert result.location == "Nice"
        assert result.participants_number == 50


class TestAssignSupport:
    def test_assign_support_updates_collaborator(self, service, session, sample_event, other_support):
        result = service.assign_support(sample_event.id, other_support.email)
        assert result is not None
        assert result.support_id == other_support.id

    def test_assign_support_persists_to_db(self, service, session, sample_event, other_support):
        service.assign_support(sample_event.id, other_support.email)
        session.expire(sample_event)
        refreshed = session.get(Event, sample_event.id)
        assert refreshed.support_id == other_support.id

    def test_assign_support_unknown_event_returns_none(self, service, support_user):
        result = service.assign_support(99999, support_user.id)
        assert result is None

    def test_assign_support_unknown_collaborator_returns_none(self, service, sample_event):
        result = service.assign_support(sample_event.id, 99999)
        assert result is None
