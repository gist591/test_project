from abc import abstractmethod
from typing import List

from src.domain.repositories import BaseRepository
from src.domain.entities import OperatorSource


class OperatorSourceRepository(BaseRepository[OperatorSource]):
    @abstractmethod
    def get_by_source_id(self, source_id: int) -> List[OperatorSource]:
        pass

    @abstractmethod
    def get_by_operator_id(self, operator_id: int) -> List[OperatorSource]:
        pass

    @abstractmethod
    def delete(self, operator_id: int, source_id: int) -> bool:
        pass
