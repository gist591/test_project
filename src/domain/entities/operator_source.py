from dataclasses import dataclass
from typing import Optional


@dataclass
class OperatorSource:
    """Source/bot - the channel from which requests come"""
    id: Optional[int]
    name: str
    is_active: bool = True
