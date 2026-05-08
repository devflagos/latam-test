from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class InputPort(ABC, Generic[T]):
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> T:
        pass
