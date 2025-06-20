from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mrfixit.adapters.database.base import BaseTable, IdentifableMixin, TimestampedMixin
from mrfixit.adapters.database.utils import make_pg_enum
from mrfixit.domains.entities.tech_request import (
    TechRequestBuilding,
    TechRequestCategory,
    TechRequestStatus,
)


class TechRequestTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "tech_requests"

    title: Mapped[str] = mapped_column(String(63), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    category: Mapped[TechRequestCategory] = mapped_column(
        make_pg_enum(TechRequestCategory, name="tech_request_category"),
        nullable=False,
    )
    status: Mapped[TechRequestStatus] = mapped_column(
        make_pg_enum(TechRequestStatus, name="tech_request_status"),
        nullable=False,
    )
    building: Mapped[TechRequestBuilding] = mapped_column(
        make_pg_enum(TechRequestBuilding, name="tech_request_building"),
        nullable=False,
    )
    file_id: Mapped[str] = mapped_column(String(512), nullable=False)
