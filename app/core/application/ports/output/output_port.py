from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class OutputPort(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def find_all(self) -> list[T]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass