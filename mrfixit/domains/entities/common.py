from collections.abc import Mapping
from dataclasses import dataclass, fields
from typing import Any

from mrfixit.application.entities import Unset


@dataclass(frozen=True, kw_only=True, slots=True)
class Pagination:
    limit: int
    offset: int


@dataclass(frozen=True, kw_only=True, slots=True)
class ToDictMixin:
    def to_dict(self) -> Mapping[str, Any]:
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if field.name != "id" and not isinstance(getattr(self, field.name), Unset)
        }
