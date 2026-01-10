from abc import abstractmethod
from typing import List

from src.domain.repositories import BaseRepository
from src.domain.entities import Contact


class ContactRepository(BaseRepository[Contact]):
    @abstractmethod
    def get_by_lead_id(self, lead_id: int) -> List[Contact]:
        pass

    @abstractmethod
    def get_by_operator_id(self, operator_id: int) -> List[Contact]:
        pass

    @abstractmethod
    def count_active_by_operator(self, operator_id: int) -> int:
        pass
