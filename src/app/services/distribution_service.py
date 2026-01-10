import random
from typing import List, Optional, Tuple

from src.domain.entities import Contact, ContactStatus, Lead, Operator


class LeadDistributionService:
    def __init__(
        self,
        operator_repo,
        lead_repo,
        source_repo,
        contact_repo,
        operator_source_repo
    ) -> None:
        self._operator_repo = operator_repo
        self._lead_repo = lead_repo
        self._source_repo = source_repo
        self._contact_repo = contact_repo
        self._operator_source_repo = operator_source_repo

    def find_or_create_lead(
        self,
        external_id: str,
        name: Optional[str] = None
    ) -> Lead:
        """Find lead for external_id or create new"""
        existing = self._lead_repo.get_by_external_id(
            external_id
        )
        if existing:
            return existing

        new_lead = Lead(
            id=None,
            external_id=external_id,
            name=name,
        )
        return self._lead_repo.add(new_lead)

    def select_operator_for_source(
        self,
        source_id: int
    ) -> Optional[Operator]:
        """Select opertor for source by weight"""
        available = self._get_available_operators(source_id)

        if not available:
            return None

        if len(available) == 1:
            return available[0][0]

        operators = [op for op, _ in available]
        weights = [weight for _, weight in available]

        return random.choices(operators, weights=weights, k=1)[0]

    def create_contact(
        self,
        external_lead_id: str,
        source_id: int,
        message: Optional[str] = None,
        lead_name: Optional[str] = None,
    ) -> Contact:
        """Create contact: find/create lead, assign operator"""
        source = self._source_repo.get_by_id(source_id)
        if not source:
            raise ValueError(f"Source with id={source_id} not found")

        lead = self.find_or_create_lead(external_id=external_lead_id, name=lead_name)

        operator = self.select_operator_for_source(source_id)

        contact = Contact(
            id=None,
            lead_id=lead.id,
            source_id=source_id,
            operator_id=operator.id if operator else None,
            status=ContactStatus.ACTIVE if operator else ContactStatus.UNASSIGNED,
            message=message,
        )

        return self._contact_repo.add(contact)

    def _get_available_operators(
        self,
        source_id: int
    ) -> List[Tuple[Operator, int]]:
        """Get available operators with weights"""
        operator_sources = self._operator_source_repo.get_by_soucre_id(source_id)
        contacts = self._contact_repo.get_all()

        result = list()
        for os in operator_sources:
            operator = self._operator_repo.get_by_id(os.operator_id)
            if not operator or not operator.is_active:
                continue

            active_count = sum(
                1 for c in contacts
                if c.operator_id == operator.id and c.status == ContactStatus.ACTIVE
            )

            if active_count < operator.max_load:
                operator.current_load = active_count
                result.append((operator, os.weight))

        return result
