from uuid import UUID

from mrfixit.application.exceptions import EntityNotFoundException
from mrfixit.domains.entities.tech_request import (
    CreateTechRequest,
    DeleteTechRequsetList,
    TechRequest,
    TechRequestList,
    TechRequestListParams,
    UpdateTechRequest,
)
from mrfixit.domains.interfaces.storages.tech_request import ITechRequestStorage


class TechRequestService:
    __tech_request_storage: ITechRequestStorage

    def __init__(self, tech_request_storage: ITechRequestStorage) -> None:
        self.__tech_request_storage = tech_request_storage

    async def create(self, *, input_dto: CreateTechRequest) -> TechRequest:
        return await self.__tech_request_storage.create(input_dto=input_dto)

    async def get_by_id(self, *, input_id: UUID) -> TechRequest:
        user = await self.__tech_request_storage.get_by_id(input_id=input_id)
        if user is None:
            raise EntityNotFoundException(entity=TechRequest, entity_id=input_id)
        return user

    async def get_list(self, *, input_dto: TechRequestListParams) -> TechRequestList:
        total = await self.__tech_request_storage.count(input_dto=input_dto)
        items = await self.__tech_request_storage.get_list(input_dto=input_dto)
        return TechRequestList(total=total, items=items)

    async def update_by_id(self, *, input_dto: UpdateTechRequest) -> TechRequest:
        return await self.__tech_request_storage.update_by_id(input_dto=input_dto)

    async def delete_list(self, *, input_dto: DeleteTechRequsetList) -> None:
        await self.__tech_request_storage.delete_list(input_dto=input_dto)
