from datetime import datetime
import pytest


from src.domain.entities import Lead


class TestLead:
    @pytest.fixture
    def lead(self) -> Lead:
        return Lead(
            id=1,
            external_id='@telegram_id_1'
        )

    def test_create_lead_with_external_id(self, lead) -> None:
        """Lead must be created with external id"""
        assert lead.id == 1
        assert lead.external_id == '@telegram_id_1'

    def test_lead_optional_name(self, lead) -> None:
        """Check that lead's name is optional"""
        lead.name = "Test name"

        assert lead.name == "Test name"

    def test_lead_has_created_at(self, lead) -> None:
        """Check that lead have a create date"""
        assert isinstance(lead.created_at, datetime)
