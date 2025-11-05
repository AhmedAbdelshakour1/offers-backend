from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_superadmin
from app.db.session import get_db
from app.models.offers import Offer
from app.schemas.offers import OfferOut
from app.services.storage import save_upload

router = APIRouter(prefix="/offers", tags=["offers"], dependencies=[Depends(require_superadmin)])


@router.post("/", response_model=OfferOut)
async def create_offer(
    headline: str = Form(...),
    description: str | None = Form(None),
    discount: float | None = Form(None),
    parent_link: str | None = Form(None),
    child_link: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = save_upload(image, subdir="images") if image else None
    item = Offer(
        headline=headline,
        description=description,
        image_url=image_url,
        discount=discount,
        parent_link=parent_link,
        child_link=child_link,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=List[OfferOut])
async def list_offers(db: Session = Depends(get_db)):
    return db.query(Offer).order_by(Offer.id.desc()).all()


@router.get("/{item_id}", response_model=OfferOut)
async def get_offer(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Offer, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return item


@router.put("/{item_id}", response_model=OfferOut)
async def update_offer(
    item_id: int,
    headline: str | None = Form(None),
    description: str | None = Form(None),
    discount: float | None = Form(None),
    parent_link: str | None = Form(None),
    child_link: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    item = db.get(Offer, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if headline is not None:
        item.headline = headline
    if description is not None:
        item.description = description
    if discount is not None:
        item.discount = discount
    if parent_link is not None:
        item.parent_link = parent_link
    if child_link is not None:
        item.child_link = child_link
    if image is not None:
        item.image_url = save_upload(image, subdir="images")

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
async def delete_offer(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Offer, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(item)
    db.commit()
    return {"status": "deleted"}
