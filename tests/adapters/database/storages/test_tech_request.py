from collections.abc import Callable
from datetime import timedelta
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from mrfixit.adapters.database.storages.tech_request import TechRequestStorage
from mrfixit.adapters.database.tables import TechRequestTable
from mrfixit.application.exceptions import (
    EntityNotFoundException,
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
from tests.utils import now_utc


async def test__create(
    tech_request_storage: TechRequestStorage,
) -> None:
    create_data = CreateTechRequest(
        title="test_title",
        description="test_description",
        category=TechRequestCategory.URGENT,
        status=TechRequestStatus.CREATED,
        building=TechRequestBuilding.FOUNTAIN,
        file_id="test_file_id",
    )
    user = await tech_request_storage.create(input_dto=create_data)
    assert user == TechRequest(
        id=IsUUID,
        title=create_data.title,
        description=create_data.description,
        category=create_data.category,
        status=create_data.status,
        building=create_data.building,
        file_id=create_data.file_id,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_by_id(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
) -> None:
    db_tech_request: TechRequestTable = await create_tech_request()
    tech_request = await tech_request_storage.get_by_id(input_id=db_tech_request.id)
    assert tech_request == TechRequest(
        id=db_tech_request.id,
        title=db_tech_request.title,
        description=db_tech_request.description,
        category=db_tech_request.category,
        status=db_tech_request.status,
        building=db_tech_request.building,
        file_id=db_tech_request.file_id,
        created_at=db_tech_request.created_at,
        updated_at=db_tech_request.updated_at,
    )


async def test__get_by_id__none(
    tech_request_storage: TechRequestStorage,
) -> None:
    assert await tech_request_storage.get_by_id(input_id=uuid4()) is None


async def test__get_list(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
) -> None:
    parameters = (
        dict(
            category=TechRequestCategory.URGENT,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.DONE,
        ),
        dict(
            category=TechRequestCategory.URGENT,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.DONE,
        ),
    )
    db_tech_requests: list[TechRequestTable] = [
        await create_tech_request(**p) for p in parameters
    ]
    tech_requests = await tech_request_storage.get_list(
        input_dto=TechRequestListParams(limit=10, offset=0)
    )
    assert tech_requests == [
        TechRequest(
            id=db_tech_request.id,
            title=db_tech_request.title,
            description=db_tech_request.description,
            category=db_tech_request.category,
            status=db_tech_request.status,
            building=db_tech_request.building,
            file_id=db_tech_request.file_id,
            created_at=db_tech_request.created_at,
            updated_at=db_tech_request.updated_at,
        )
        for db_tech_request in db_tech_requests
    ]


async def test__get_list__validate_limit(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
) -> None:
    parameters = (
        dict(
            category=TechRequestCategory.URGENT,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.DONE,
        ),
        dict(
            category=TechRequestCategory.URGENT,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.DONE,
        ),
    )
    db_tech_requests: list[TechRequestTable] = [
        await create_tech_request(**p) for p in parameters
    ]
    tech_requests = await tech_request_storage.get_list(
        input_dto=TechRequestListParams(limit=3, offset=0)
    )
    assert (
        tech_requests
        == [
            TechRequest(
                id=db_tech_request.id,
                title=db_tech_request.title,
                description=db_tech_request.description,
                category=db_tech_request.category,
                status=db_tech_request.status,
                building=db_tech_request.building,
                file_id=db_tech_request.file_id,
                created_at=db_tech_request.created_at,
                updated_at=db_tech_request.updated_at,
            )
            for db_tech_request in db_tech_requests
        ][:3]
    )


async def test__get_list__validate_offset(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
) -> None:
    parameters = (
        dict(
            category=TechRequestCategory.URGENT,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FOUNTAIN,
            status=TechRequestStatus.DONE,
        ),
        dict(
            category=TechRequestCategory.URGENT,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.CREATED,
        ),
        dict(
            category=TechRequestCategory.ORDINARY,
            building=TechRequestBuilding.FORT_DIALOG,
            status=TechRequestStatus.DONE,
        ),
    )
    db_tech_requests: list[TechRequestTable] = [
        await create_tech_request(**p) for p in parameters
    ]
    tech_requests = await tech_request_storage.get_list(
        input_dto=TechRequestListParams(limit=10, offset=3)
    )
    assert (
        tech_requests
        == [
            TechRequest(
                id=db_tech_request.id,
                title=db_tech_request.title,
                description=db_tech_request.description,
                category=db_tech_request.category,
                status=db_tech_request.status,
                building=db_tech_request.building,
                file_id=db_tech_request.file_id,
                created_at=db_tech_request.created_at,
                updated_at=db_tech_request.updated_at,
            )
            for db_tech_request in db_tech_requests
        ][3:]
    )


async def test__get_list__empty_list(
    tech_request_storage: TechRequestStorage,
) -> None:
    tech_requests = await tech_request_storage.get_list(
        input_dto=TechRequestListParams(limit=10, offset=0)
    )
    assert tech_requests == []


async def test__count(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
) -> None:
    await create_tech_request()
    assert (
        await tech_request_storage.count(
            input_dto=TechRequestListParams(limit=10, offset=0)
        )
        == 1
    )


async def test__count__zero(
    tech_request_storage: TechRequestStorage,
) -> None:
    assert (
        await tech_request_storage.count(
            input_dto=TechRequestListParams(limit=10, offset=0)
        )
        == 0
    )


async def test__exists_by_id(
    tech_request_storage: TechRequestStorage, create_tech_request: Callable
) -> None:
    db_tech_request: TechRequestTable = await create_tech_request()
    assert await tech_request_storage.exists_by_id(input_id=db_tech_request.id)


async def test__exists_by_id__false(
    tech_request_storage: TechRequestStorage,
) -> None:
    assert not await tech_request_storage.exists_by_id(input_id=uuid4())


async def test__update_by_id(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
) -> None:
    db_tech_request: TechRequestTable = await create_tech_request()
    update_data = UpdateTechRequest(
        id=db_tech_request.id,
        title="test_title",
        description="test_description",
        category=TechRequestCategory.URGENT,
        status=TechRequestStatus.CREATED,
        building=TechRequestBuilding.FOUNTAIN,
        file_id="test_file_id",
    )
    tech_request = await tech_request_storage.update_by_id(input_dto=update_data)
    assert tech_request == TechRequest(
        id=update_data.id,
        title=update_data.title,
        description=update_data.description,
        category=update_data.category,
        status=update_data.status,
        building=update_data.building,
        file_id=update_data.file_id,
        created_at=db_tech_request.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    tech_request_storage: TechRequestStorage,
) -> None:
    update_data = UpdateTechRequest(
        id=uuid4(),
        title="test_title",
        description="test_description",
        category=TechRequestCategory.URGENT,
        status=TechRequestStatus.CREATED,
        building=TechRequestBuilding.FOUNTAIN,
        file_id="test_file_id",
    )
    with pytest.raises(EntityNotFoundException):
        await tech_request_storage.update_by_id(input_dto=update_data)


async def test__delete_list(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
    session: AsyncSession,
) -> None:
    [await create_tech_request() for _ in range(2)]
    await tech_request_storage.delete_list(
        input_dto=DeleteTechRequsetList(created_at=None, status=None)
    )
    count = await session.scalar(select(func.count()).select_from(TechRequestTable))
    assert count == 0


async def test__delete_list__validate_created_at(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
    session: AsyncSession,
) -> None:
    await create_tech_request()
    await create_tech_request(created_at=now_utc() - timedelta(days=2))
    await tech_request_storage.delete_list(
        input_dto=DeleteTechRequsetList(
            created_at=now_utc() - timedelta(days=1), status=None
        )
    )
    count = await session.scalar(select(func.count()).select_from(TechRequestTable))
    assert count == 1


async def test__delete_list__validate_status(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
    session: AsyncSession,
) -> None:
    status = TechRequestStatus.DONE
    await create_tech_request(status=TechRequestStatus.CREATED)
    db_tech_request: TechRequestTable = await create_tech_request(status=status)
    await tech_request_storage.delete_list(
        input_dto=DeleteTechRequsetList(created_at=None, status=db_tech_request.status)
    )
    count = await session.scalar(select(func.count()).select_from(TechRequestTable))
    assert count == 1


async def test__delete_list__validate_status_and_created_at(
    tech_request_storage: TechRequestStorage,
    create_tech_request: Callable,
    session: AsyncSession,
) -> None:
    status = TechRequestStatus.DONE
    await create_tech_request(status=TechRequestStatus.CREATED)
    db_tech_request: TechRequestTable = await create_tech_request(
        status=status,
        created_at=now_utc() - timedelta(days=2),
    )
    await tech_request_storage.delete_list(
        input_dto=DeleteTechRequsetList(
            created_at=now_utc() - timedelta(days=1),
            status=db_tech_request.status,
        )
    )
    count = await session.scalar(select(func.count()).select_from(TechRequestTable))
    assert count == 1
