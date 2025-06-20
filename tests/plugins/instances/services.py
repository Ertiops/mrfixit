import pytest

from mrfixit.domains.interfaces.storages.tech_request import ITechRequestStorage
from mrfixit.domains.services.tech_request import TechRequestService


@pytest.fixture
def tech_request_service(
    tech_request_storage: ITechRequestStorage,
) -> TechRequestService:
    return TechRequestService(tech_request_storage=tech_request_storage)
