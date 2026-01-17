from dataclasses import dataclass, field
from datetime import datetime

from src.domain.entities.contact_status import ContactStatus


@dataclass
class Contact:
    """A conversion is the fact of a lead's contact through a source"""

    id: int | None
    lead_id: int
    source_id: int
    operator_id: int | None = None
    status: ContactStatus = ContactStatus.ACTIVE
    message: str | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def is_active(self) -> bool:
        """Is the request is active"""
        return self.status == ContactStatus.ACTIVE
