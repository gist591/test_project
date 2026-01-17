from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class BaseRepository[T](ABC):
    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass
