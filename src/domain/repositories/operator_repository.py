from abc import abstractmethod

from src.domain.entities import Operator
from src.domain.repositories import BaseRepository


class OperatorRepository(BaseRepository[Operator]):
    @abstractmethod
    def get_available_for_source(self, source_id: int) -> list[tuple[Operator, int]]:
        """Get available operators from source with weight"""
        pass
