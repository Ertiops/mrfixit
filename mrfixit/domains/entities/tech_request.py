from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, unique
from uuid import UUID

from mrfixit.application.entities import UNSET, Unset
from mrfixit.domains.entities.common import Pagination, ToDictMixin


@unique
class TechRequestCategory(StrEnum):
    ORDINARY = "ordinary"
    URGENT = "urgent"


@unique
class TechRequestStatus(StrEnum):
    CREATED = "created"
    DONE = "done"


@unique
class TechRequestBuilding(StrEnum):
    FOUNTAIN = "fontan"
    FORT_DIALOG = "fort_dialog"


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateTechRequest(ToDictMixin):
    title: str
    description: str
    category: TechRequestCategory
    status: TechRequestStatus
    building: TechRequestBuilding
    file_id: str


@dataclass(frozen=True, kw_only=True, slots=True)
class TechRequest:
    id: UUID
    title: str
    description: str
    category: TechRequestCategory
    status: TechRequestStatus
    building: TechRequestBuilding
    file_id: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class TechRequestListParams(Pagination): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class TechRequestList:
    total: int
    items: Sequence[TechRequest]


@dataclass(frozen=True, kw_only=True, slots=True)
class DeleteTechRequsetList:
    created_at: datetime | None
    status: TechRequestStatus | None


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateTechRequest(ToDictMixin):
    id: UUID
    title: str | Unset = UNSET
    description: str | Unset = UNSET
    category: TechRequestCategory | Unset = UNSET
    status: TechRequestStatus | Unset = UNSET
    building: TechRequestBuilding | Unset = UNSET
    file_id: str | Unset = UNSET
