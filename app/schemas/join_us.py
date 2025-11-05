from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class JoinUsCreate(BaseModel):
    name: str
    mobile_number: Optional[str] = None
    email: Optional[str] = None


class JoinUsOut(BaseModel):
    id: int
    name: str
    mobile_number: Optional[str] = None
    email: Optional[str] = None
    cv_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
