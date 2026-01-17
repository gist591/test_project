from abc import abstractmethod

from src.domain.entities import Lead
from src.domain.repositories import BaseRepository


class LeadRepository(BaseRepository[Lead]):
    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Lead | None:
        pass
