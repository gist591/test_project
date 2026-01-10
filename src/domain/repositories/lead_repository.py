from abc import abstractmethod
from typing import Optional

from src.domain.repositories import BaseRepository
from src.domain.entities import Lead

class LeadRepository(BaseRepository[Lead]):
    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Optional[Lead]:
        pass
