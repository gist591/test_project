from abc import abstractmethod
from typing import List, Tuple


from src.domain.repositories import BaseRepostiory
from src.domain.entities import Operator


class OperatorRepository(BaseRepostiory[Operator]):
    @abstractmethod
    def get_available_for_source(self, source_id: int) -> List[Tuple[Operator, int]]:
        """Get available operators from source with weight"""
        pass
