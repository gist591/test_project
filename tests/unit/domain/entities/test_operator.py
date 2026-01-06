import pytest

from src.domain.entities import Operator


class TestOperator:
    @pytest.fixture
    def operator(self) -> Operator:
        return Operator(id=1, name="Test name")

    """Tests for entity Operator"""
    def test_create_operator_with_name(self, operator) -> None:
        """The operator must be created with name"""
        assert operator.id == 1
        assert operator.name == "Test name"

    def test_operator_default_values(self, operator) -> None:
        """The operator must be by default is active and have limit 10"""
        assert operator.is_active is True
        assert operator.max_load == 10
        assert operator.current_load == 0

    def test_can_accept_lead_when_active_and_has_capactiry(self, operator) -> None:
        """The active operator without leads may accept lead"""
        operator.current_load=5
        assert operator.can_accept_lead() is True

    def test_cannot_accept_lead_when_inactive(self, operator) -> None:
        """The inactive ooperator can't accept lead"""
        operator.is_active = False

        assert operator.can_accept_lead() is False

    def test_cannot_accept_lead_when_at_capactiy(self, operator) -> None:
        """The operator with an exhausted limit cannot accept a lead"""
        operator.max_load = 5
        operator.current_load = 5

        assert operator.can_accept_lead() is False
