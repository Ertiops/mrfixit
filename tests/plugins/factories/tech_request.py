from collections.abc import Callable
from datetime import datetime

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from mrfixit.adapters.database.tables import TechRequestTable
from tests.utils import now_utc


class TechRequestTableFactory(SQLAlchemyFactory[TechRequestTable]):
    @classmethod
    def created_at(cls) -> datetime:
        return now_utc()

    @classmethod
    def deleted_at(cls) -> None:
        return None


@pytest.fixture
def create_tech_request(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> TechRequestTable:
        tech_request: TechRequestTable = TechRequestTableFactory.build(**kwargs)
        session.add(tech_request)
        await session.commit()
        await session.refresh(tech_request)
        return tech_request

    return _factory
