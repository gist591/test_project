import pytest

from src.domain.entities import Contact
from src.domain.entities import ContactStatus


class TestConact:
    @pytest.fixture
    def contact(self) -> Contact:
        return Contact(
            id=1,
            lead_id=10,
            source_id=20,
            operator_id=30,
        )

    def test_create_contact(self, contact) -> None:
        """The test connects the cover, the source and the operator"""
        assert contact.id == 1
        assert contact.lead_id == 10
        assert contact.source_id == 20
        assert contact.operator_id == 30

    def test_contact_can_be_unassigned(self, contact) -> None:
        """The test connects may be without operator"""
        contact.operator_id = None
        assert contact.operator_id is None

    def test_contact_default_status_is_active(self, contact) -> None:
        """The test by default, the request is active"""
        assert contact.status == ContactStatus.ACTIVE

    def test_contact_is_active_method(self, contact) -> None:
        """The test method is_active return True for active requests"""
        contact.status = ContactStatus.ACTIVE
        assert contact.is_active() is True

        contact.status = ContactStatus.COMPLETED
        assert contact.is_active() is False
