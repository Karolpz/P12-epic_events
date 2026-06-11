import pytest
from epicevent.models import Collaborator, RoleEnum


def _make_collab():
    return Collaborator(name="Test User", email="test@test.com", role=RoleEnum.commercial)


class TestSetPassword:
    def test_password_is_hashed(self):
        collab = _make_collab()
        collab.set_password("plainpassword")
        assert collab.password != "plainpassword"

    def test_hashed_password_is_not_empty(self):
        collab = _make_collab()
        collab.set_password("secret")
        assert collab.password and len(collab.password) > 20

    def test_two_calls_produce_different_hashes(self):
        collab = _make_collab()
        collab.set_password("same_password")
        hash1 = collab.password
        collab.set_password("same_password")
        hash2 = collab.password
        # Argon2 uses random salt so hashes differ even for same input
        assert hash1 != hash2


class TestVerifyPassword:
    def test_correct_password_returns_true(self):
        collab = _make_collab()
        collab.set_password("correct_password")
        assert collab.verify_password("correct_password") is True

    def test_wrong_password_returns_false(self):
        collab = _make_collab()
        collab.set_password("correct_password")
        assert collab.verify_password("wrong_password") is False

    def test_empty_password_returns_false(self):
        collab = _make_collab()
        collab.set_password("correct_password")
        assert collab.verify_password("") is False

    def test_partial_password_returns_false(self):
        collab = _make_collab()
        collab.set_password("correct_password")
        assert collab.verify_password("correct") is False

    def test_verify_after_password_change_uses_new_hash(self):
        collab = _make_collab()
        collab.set_password("old_password")
        collab.set_password("new_password")
        assert collab.verify_password("old_password") is False
        assert collab.verify_password("new_password") is True
