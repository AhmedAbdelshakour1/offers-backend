from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict


class OfferBase(BaseModel):
    headline: str
    description: Optional[str] = None
    discount: Optional[float] = None
    parent_link: Optional[str] = None
    child_link: Optional[str] = None


class OfferCreate(OfferBase):
    pass


class OfferUpdate(BaseModel):
    headline: Optional[str] = None
    description: Optional[str] = None
    discount: Optional[float] = None
    parent_link: Optional[str] = None
    child_link: Optional[str] = None
    order_id: Optional[int] = None


class OfferOut(OfferBase):
    id: int
    image_url: Optional[str] = None
    order_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
