from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Lead:
    """Lead - is potential client"""
    id: Optional[int]
    external_id: str
    name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
