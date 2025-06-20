from mrfixit.adapters.database.tables import TechRequestTable
from mrfixit.domains.entities.tech_request import TechRequest


def convert_tech_request(
    *,
    result: TechRequestTable,
) -> TechRequest:
    return TechRequest(
        id=result.id,
        title=result.title,
        description=result.description,
        category=result.category,
        status=result.status,
        building=result.building,
        file_id=result.file_id,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
