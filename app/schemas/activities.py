from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ActivityCreate(BaseModel):
    headline: str
    description: Optional[str] = None
    date: Optional[date] = None
    link: Optional[str] = None


class ActivityUpdate(BaseModel):
    headline: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    link: Optional[str] = None


class ActivityOut(BaseModel):
    id: int
    headline: str
    description: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    image_url: Optional[str] = None
    order_id: Optional[int] = None


    model_config = ConfigDict(from_attributes=True)
