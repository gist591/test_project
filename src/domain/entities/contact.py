from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.entities.contact_status import ContactStatus


@dataclass
class Contact:
    """A conversion is the fact of a lead's contact through a source"""
    id: Optional[int]
    lead_id: int
    source_id: int
    operator_id: Optional[int] = None
    status: ContactStatus = ContactStatus.ACTIVE
    message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def is_active(self) -> bool:
        """Is the request is active"""
        return self.status == ContactStatus.ACTIVE
