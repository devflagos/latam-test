from typing import Any, Optional
from uuid import UUID, uuid4
from datetime import datetime


class Entity:
    def __init__(self, id: Optional[UUID] = None) -> None:
        self._id = id if id is not None else uuid4()
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def _set_updated_at(self) -> None:
        self._updated_at = datetime.now()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)