from collections.abc import Sequence
from typing import NoReturn
from uuid import UUID

from sqlalchemy import Date, case, cast, delete, exists, func, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from mrfixit.adapters.database.converters.tech_request import convert_tech_request
from mrfixit.adapters.database.tables import TechRequestTable
from mrfixit.application.exceptions import (
    EntityNotFoundException,
    StorageException,
)
from mrfixit.domains.entities.tech_request import (
    CreateTechRequest,
    DeleteTechRequsetList,
    TechRequest,
    TechRequestBuilding,
    TechRequestCategory,
    TechRequestListParams,
    TechRequestStatus,
    UpdateTechRequest,
)
from mrfixit.domains.interfaces.storages.tech_request import ITechRequestStorage


class TechRequestStorage(ITechRequestStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateTechRequest) -> TechRequest:
        stmt = (
            insert(TechRequestTable)
            .values(**input_dto.to_dict())
            .returning(TechRequestTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_tech_request(result=result)

    async def get_by_id(self, *, input_id: UUID) -> TechRequest | None:
        stmt = select(TechRequestTable).where(
            TechRequestTable.id == input_id, TechRequestTable.deleted_at.is_(None)
        )
        result = await self.__session.scalar(stmt)
        return convert_tech_request(result=result) if result else None

    async def get_list(
        self, *, input_dto: TechRequestListParams
    ) -> Sequence[TechRequest]:
        stmt = (
            select(TechRequestTable)
            .where(TechRequestTable.deleted_at.is_(None))
            .order_by(
                case(
                    (TechRequestTable.building == TechRequestBuilding.FOUNTAIN, 0),
                    (TechRequestTable.building == TechRequestBuilding.FORT_DIALOG, 1),
                ),
                case(
                    (TechRequestTable.category == TechRequestCategory.URGENT, 0),
                    (TechRequestTable.category == TechRequestCategory.ORDINARY, 1),
                ),
                case(
                    (TechRequestTable.status == TechRequestStatus.DONE, 1),
                    else_=0,
                ),
                TechRequestTable.created_at.asc(),
            )
            .limit(input_dto.limit)
            .offset(input_dto.offset)
        )
        result = await self.__session.scalars(stmt)
        return [convert_tech_request(result=r) for r in result]

    async def count(self, *, input_dto: TechRequestListParams) -> int:
        stmt = (
            select(func.count())
            .select_from(TechRequestTable)
            .where(TechRequestTable.deleted_at.is_(None))
        )
        return await self.__session.scalar(stmt) or 0

    async def exists_by_id(self, *, input_id: UUID) -> bool:
        stmt = select(
            exists().where(
                TechRequestTable.id == input_id, TechRequestTable.deleted_at.is_(None)
            )
        )
        return bool(await self.__session.scalar(stmt))

    async def update_by_id(self, *, input_dto: UpdateTechRequest) -> TechRequest:
        stmt = (
            update(TechRequestTable)
            .where(TechRequestTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(TechRequestTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(
                entity=TechRequest, entity_id=input_dto.id
            ) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_tech_request(result=result)

    async def delete_list(self, *, input_dto: DeleteTechRequsetList) -> None:
        stmt = delete(TechRequestTable)
        if input_dto.status:
            stmt = stmt.where(TechRequestTable.status == input_dto.status)
        if input_dto.created_at:
            stmt = stmt.where(
                cast(TechRequestTable.created_at, Date) < input_dto.created_at.date()
            )
        await self.__session.execute(stmt)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        raise StorageException(self.__class__.__name__) from e
