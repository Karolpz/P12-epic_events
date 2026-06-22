import os
import pytest
import jwt
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

from epicevent.utils.token import generate_token, verify_token, get_token, delete_token
from epicevent.utils.token import refresh_token as refresh_token_func

SECRET = "test-secret-key-for-pytest-32chars!"


@pytest.fixture(autouse=True)
def clean_token_files():
    for path in [".token", ".refresh_token"]:
        if os.path.exists(path):
            os.remove(path)
    yield
    for path in [".token", ".refresh_token"]:
        if os.path.exists(path):
            os.remove(path)


class TestGenerateToken:
    def test_returns_string(self, commercial_user):
        token = generate_token(commercial_user)
        assert isinstance(token, str)

    def test_writes_token_file(self, commercial_user):
        generate_token(commercial_user)
        assert os.path.exists(".token")

    def test_writes_refresh_token_file(self, commercial_user):
        generate_token(commercial_user)
        assert os.path.exists(".refresh_token")

    def test_token_contains_collaborator_id(self, commercial_user):
        token = generate_token(commercial_user)
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        assert payload["collaborator"]["id"] == commercial_user.id

    def test_token_contains_role(self, commercial_user):
        token = generate_token(commercial_user)
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        assert payload["collaborator"]["role"] == commercial_user.role.value

    def test_access_token_expires_in_15_minutes(self, commercial_user):
        before = datetime.now(timezone.utc) + timedelta(minutes=14)
        token = generate_token(commercial_user)
        after = datetime.now(timezone.utc) + timedelta(minutes=16)
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert before <= exp <= after

    def test_refresh_token_expires_in_7_days(self, commercial_user):
        generate_token(commercial_user)
        with open(".refresh_token") as f:
            refresh = f.read()
        payload = jwt.decode(refresh, SECRET, algorithms=["HS256"])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected = datetime.now(timezone.utc) + timedelta(days=6)
        assert exp > expected


class TestVerifyToken:
    def test_valid_token_returns_collaborator_data(self, commercial_user):
        token = generate_token(commercial_user)
        result = verify_token(token)
        assert result is not None
        assert result["id"] == commercial_user.id
        assert result["role"] == commercial_user.role.value

    def test_invalid_token_returns_none(self):
        result = verify_token("not.a.valid.token")
        assert result is None

    def test_tampered_token_returns_none(self, commercial_user):
        token = generate_token(commercial_user) + "xyz"
        result = verify_token(token)
        assert result is None

    def test_wrong_secret_returns_none(self, commercial_user):
        payload = {
            "collaborator": {"id": commercial_user.id, "role": commercial_user.role.value},
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        }
        bad_token = jwt.encode(payload, "wrong-secret", algorithm="HS256")
        result = verify_token(bad_token)
        assert result is None

    def test_expired_token_calls_refresh(self, commercial_user):
        expired_token = jwt.encode(
            {
                "collaborator": {"id": commercial_user.id, "role": commercial_user.role.value},
                "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
            },
            SECRET,
            algorithm="HS256",
        )
        with patch("epicevent.utils.token.refresh_token", return_value=None) as mock_refresh:
            verify_token(expired_token)
            mock_refresh.assert_called_once()


class TestGetToken:
    def test_returns_token_when_file_exists(self, commercial_user):
        generate_token(commercial_user)
        assert get_token() is not None

    def test_returned_value_matches_generated_token(self, commercial_user):
        token = generate_token(commercial_user)
        assert get_token() == token

    def test_returns_none_when_no_file(self):
        assert get_token() is None


class TestDeleteToken:
    def test_removes_token_file(self, commercial_user):
        generate_token(commercial_user)
        delete_token()
        assert not os.path.exists(".token")

    def test_removes_refresh_token_file(self, commercial_user):
        generate_token(commercial_user)
        delete_token()
        assert not os.path.exists(".refresh_token")

    def test_returns_true_even_without_files(self):
        result = delete_token()
        assert result is True

    def test_token_no_longer_valid_after_delete(self, commercial_user):
        generate_token(commercial_user)
        delete_token()
        assert get_token() is None


class TestRefreshToken:
    def test_returns_collaborator_payload_with_valid_refresh_token(self, commercial_user):
        generate_token(commercial_user)
        with patch("epicevent.utils.token.Session") as MockSession:
            mock_session = MockSession.return_value.__enter__.return_value
            mock_session.query.return_value.filter_by.return_value.first.return_value = commercial_user
            result = refresh_token_func()
        assert result is not None
        assert result["id"] == commercial_user.id

    def test_returns_none_when_no_refresh_token_file(self):
        result = refresh_token_func()
        assert result is None

    def test_returns_none_when_refresh_token_expired(self, commercial_user):
        expired = jwt.encode(
            {
                "collaborator": {"id": commercial_user.id, "role": commercial_user.role.value},
                "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
            },
            SECRET,
            algorithm="HS256",
        )
        with open(".refresh_token", "w") as f:
            f.write(expired)
        result = refresh_token_func()
        assert result is None

    def test_returns_none_when_collaborator_not_found(self, commercial_user):
        generate_token(commercial_user)
        with patch("epicevent.utils.token.Session") as MockSession:
            mock_session = MockSession.return_value.__enter__.return_value
            mock_session.query.return_value.filter_by.return_value.first.return_value = None
            result = refresh_token_func()
        assert result is None

    def test_regenerates_access_token_on_refresh(self, commercial_user):
        generate_token(commercial_user)
        if os.path.exists(".token"):
            os.remove(".token")
        assert not os.path.exists(".token")
        with patch("epicevent.utils.token.Session") as MockSession:
            mock_session = MockSession.return_value.__enter__.return_value
            mock_session.query.return_value.filter_by.return_value.first.return_value = commercial_user
            refresh_token_func()
        assert os.path.exists(".token")
