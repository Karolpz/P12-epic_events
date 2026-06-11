import pytest
from unittest.mock import patch
from epicevent.models import Collaborator, RoleEnum
from epicevent.services.auth_service import AuthService


@pytest.fixture
def auth_service(session):
    return AuthService(session)


@pytest.fixture
def existing_user(session):
    user = Collaborator(name="Alice", email="alice@epic.io", role=RoleEnum.gestion)
    user.set_password("GoodPassword!")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


class TestLogin:
    def test_login_success_returns_collaborator(self, auth_service, existing_user):
        with patch("epicevent.services.auth_service.generate_token"):
            result = auth_service.login("alice@epic.io", "GoodPassword!")
        assert result is not None
        assert result.email == "alice@epic.io"

    def test_login_success_calls_generate_token(self, auth_service, existing_user):
        with patch("epicevent.services.auth_service.generate_token") as mock_token:
            auth_service.login("alice@epic.io", "GoodPassword!")
        mock_token.assert_called_once_with(existing_user)

    def test_login_wrong_password_returns_none(self, auth_service, existing_user):
        with patch("epicevent.services.auth_service.generate_token"):
            result = auth_service.login("alice@epic.io", "WrongPassword!")
        assert result is None

    def test_login_unknown_email_returns_none(self, auth_service):
        result = auth_service.login("unknown@epic.io", "GoodPassword!")
        assert result is None

    def test_login_empty_password_returns_none(self, auth_service, existing_user):
        with patch("epicevent.services.auth_service.generate_token"):
            result = auth_service.login("alice@epic.io", "")
        assert result is None
