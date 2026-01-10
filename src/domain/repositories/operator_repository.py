from abc import abstractmethod
from typing import List, Tuple


from src.domain.repositories import BaseRepository
from src.domain.entities import Operator


class OperatorRepository(BaseRepository[Operator]):
    @abstractmethod
    def get_available_for_source(self, source_id: int) -> List[Tuple[Operator, int]]:
        """Get available operators from source with weight"""
        pass
