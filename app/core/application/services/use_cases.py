from app.core.application.ports.input.input_port import InputPort
from app.core.application.ports.output.output_port import OutputPort


class ApplicationService:
    def __init__(self, repository: OutputPort) -> None:
        self._repository = repository

    @property
    def repository(self) -> OutputPort:
        return self._repository


class CreateUseCase(ApplicationService, InputPort):
    async def execute(self, entity):
        return await self._repository.save(entity)


class FindByIdUseCase(ApplicationService, InputPort):
    async def execute(self, id: str):
        return await self._repository.find_by_id(id)


class FindAllUseCase(ApplicationService, InputPort):
    async def execute(self):
        return await self._repository.find_all()


class DeleteUseCase(ApplicationService, InputPort):
    async def execute(self, id: str) -> bool:
        return await self._repository.delete(id)
