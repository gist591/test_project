from dataclasses import dataclass


@dataclass
class Operator:
    id: int | None
    name: str
    is_active: bool = True
    max_load: int = 10
    current_load: int = 0

    def can_accept_lead(self) -> bool:
        """Check, the operator can accept new appel"""
        return self.is_active and self.current_load < self.max_load
