from abc import abstractmethod

from src.domain.entities import OperatorSource
from src.domain.repositories import BaseRepository


class OperatorSourceRepository(BaseRepository[OperatorSource]):
    @abstractmethod
    def get_by_source_id(self, source_id: int) -> list[OperatorSource]:
        pass

    @abstractmethod
    def get_by_operator_id(self, operator_id: int) -> list[OperatorSource]:
        pass

    @abstractmethod
    def delete(self, operator_id: int, source_id: int) -> bool:
        pass
