from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class WaitlistCreate(BaseModel):
    email: EmailStr
    source_page: str = Field(default="unknown", min_length=1, max_length=60)
    wants_shop_signals: bool = False


class WaitlistResponse(BaseModel):
    message: str
    created: bool


class WaitlistStats(BaseModel):
    waitlist_count: int
    shops_count_teaser: int
    as_of: datetime
