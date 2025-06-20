from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from mrfixit.domains.entities.tech_request import (
    CreateTechRequest,
    DeleteTechRequsetList,
    TechRequest,
    TechRequestListParams,
    UpdateTechRequest,
)


class ITechRequestStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateTechRequest) -> TechRequest:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *, input_id: UUID) -> TechRequest | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(
        self, *, input_dto: TechRequestListParams
    ) -> Sequence[TechRequest]:
        raise NotImplementedError

    @abstractmethod
    async def count(self, *, input_dto: TechRequestListParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_id(self, *, input_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateTechRequest) -> TechRequest:
        raise NotImplementedError

    @abstractmethod
    async def delete_list(self, *, input_dto: DeleteTechRequsetList) -> None:
        raise NotImplementedError
