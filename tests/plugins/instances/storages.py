import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mrfixit.adapters.database.storages.tech_request import TechRequestStorage
from mrfixit.domains.interfaces.storages.tech_request import ITechRequestStorage


@pytest.fixture
def tech_request_storage(session: AsyncSession) -> ITechRequestStorage:
    return TechRequestStorage(session=session)
