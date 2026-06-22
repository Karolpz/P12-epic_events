import os
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test")
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-pytest-32chars!"

from epicevent.models.base import Base
from epicevent.models import Collaborator, Client, Contract, Event, RoleEnum


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def gestion_user(session):
    user = Collaborator(name="Alice Gestion", email="alice@epic.io", role=RoleEnum.gestion)
    user.set_password("Password123!")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def commercial_user(session):
    user = Collaborator(name="Lopez Commercial", email="lopez@epic.io", role=RoleEnum.commercial)
    user.set_password("Password123!")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def other_commercial(session):
    user = Collaborator(name="Autre Commercial", email="autre@epic.io", role=RoleEnum.commercial)
    user.set_password("Password123!")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def support_user(session):
    user = Collaborator(name="Dupont Support", email="dupont@epic.io", role=RoleEnum.support)
    user.set_password("Password123!")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def sample_client(session, commercial_user):
    client = Client(
        first_name="Jean",
        last_name="Martin",
        email="jean@company.com",
        company="Company SA",
        phone_number="0600000000",
        collaborator_id=commercial_user.id,
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@pytest.fixture
def unsigned_contract(session, sample_client, commercial_user):
    contract = Contract(
        amount=5000.0,
        amount_to_pay=5000.0,
        is_signed=False,
        collaborator_id=commercial_user.id,
        client_id=sample_client.id,
    )
    session.add(contract)
    session.commit()
    session.refresh(contract)
    return contract


@pytest.fixture
def signed_contract(session, sample_client, commercial_user):
    contract = Contract(
        amount=5000.0,
        amount_to_pay=5000.0,
        is_signed=True,
        collaborator_id=commercial_user.id,
        client_id=sample_client.id,
    )
    session.add(contract)
    session.commit()
    session.refresh(contract)
    return contract


@pytest.fixture
def sample_event(session, signed_contract, support_user):
    event = Event(
        title="Gala Annuel",
        location="Paris",
        start_date=datetime(2025, 9, 1, 18, 0),
        end_date=datetime(2025, 9, 1, 23, 0),
        participants_number=100,
        notes="Note de test",
        commercial_id=signed_contract.collaborator_id,
        support_id=support_user.id,
        contract_id=signed_contract.id,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
