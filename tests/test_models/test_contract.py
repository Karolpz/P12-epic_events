import pytest
from epicevent.models import Contract, Collaborator, RoleEnum


def _make_contract(is_signed=False, collaborator_id=1):
    return Contract(
        amount=1000.0,
        amount_to_pay=1000.0,
        is_signed=is_signed,
        collaborator_id=collaborator_id,
        client_id=1,
    )


def _make_collab(role, collab_id):
    collab = Collaborator(name="X", email="x@x.com", role=role)
    collab.id = collab_id
    return collab


class TestSign:
    def test_sign_sets_is_signed_true(self):
        contract = _make_contract(is_signed=False)
        contract.sign()
        assert contract.is_signed is True

    def test_sign_already_signed_raises_exception(self):
        contract = _make_contract(is_signed=True)
        with pytest.raises(Exception, match="déjà signé"):
            contract.sign()

    def test_sign_is_idempotent_raises_on_second_call(self):
        contract = _make_contract(is_signed=False)
        contract.sign()
        with pytest.raises(Exception):
            contract.sign()


class TestCanEdit:
    def test_gestion_can_edit_any_contract(self):
        contract = _make_contract(collaborator_id=5)
        gestion = _make_collab(RoleEnum.gestion, collab_id=99)
        assert contract.can_edit(gestion) is True

    def test_commercial_owner_can_edit_own_contract(self):
        contract = _make_contract(collaborator_id=5)
        commercial = _make_collab(RoleEnum.commercial, collab_id=5)
        assert contract.can_edit(commercial) is True

    def test_commercial_non_owner_cannot_edit(self):
        contract = _make_contract(collaborator_id=5)
        other_commercial = _make_collab(RoleEnum.commercial, collab_id=7)
        assert contract.can_edit(other_commercial) is False

    def test_support_cannot_edit_other_contract(self):
        contract = _make_contract(collaborator_id=5)
        support = _make_collab(RoleEnum.support, collab_id=99)
        assert contract.can_edit(support) is False
