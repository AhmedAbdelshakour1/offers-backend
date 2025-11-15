from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class NewsCreate(BaseModel):
    headline: str
    description: Optional[str] = None
    date: Optional[date] = None


class NewsUpdate(BaseModel):
    headline: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None


class NewsOut(BaseModel):
    id: int
    headline: str
    description: Optional[str] = None
    date: Optional[str] = None
    image_url: Optional[str] = None
    order_id: Optional[int] = None


    model_config = ConfigDict(from_attributes=True)
