from abc import ABC, abstractmethod


class OutputPort(ABC):
    @abstractmethod
    async def save(self, entity: object) -> object:
        pass

    @abstractmethod
    async def find_by_id(self, id: str) -> object | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[object]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
