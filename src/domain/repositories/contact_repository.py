from abc import abstractmethod

from src.domain.entities import Contact
from src.domain.repositories import BaseRepository


class ContactRepository(BaseRepository[Contact]):
    @abstractmethod
    def get_by_lead_id(self, lead_id: int) -> list[Contact]:
        pass

    @abstractmethod
    def get_by_operator_id(self, operator_id: int) -> list[Contact]:
        pass

    @abstractmethod
    def count_active_by_operator(self, operator_id: int) -> int:
        pass
