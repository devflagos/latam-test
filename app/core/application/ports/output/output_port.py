from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class OutputPort(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass

    @abstractmethod
    async def find_by_id(self, id: str) -> T | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[T]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
