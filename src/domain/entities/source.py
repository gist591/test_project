from dataclasses import dataclass


@dataclass
class Source:
    """Source/bot - the channel from which requests come"""

    id: int | None
    name: str
    is_active: bool = True
