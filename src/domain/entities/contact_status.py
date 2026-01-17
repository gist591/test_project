from enum import Enum


class ContactStatus(Enum):
    """Contact status"""

    ACTIVE = "active"
    COMPLETED = "completed"
    UNASSIGNED = "unassigned"
