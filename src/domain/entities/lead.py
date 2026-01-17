from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Lead:
    """Lead - is potential client"""

    id: int | None
    external_id: str
    name: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
