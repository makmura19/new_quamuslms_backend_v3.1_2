from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class BaseDataClassMixin:
    is_deleted: Optional[bool] = field(default=False)
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
