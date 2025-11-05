from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class KeepInTouchCreate(BaseModel):
    name: str
    mobile_number: Optional[str] = None
    email: Optional[str] = None


class KeepInTouchOut(BaseModel):
    id: int
    name: str
    mobile_number: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
