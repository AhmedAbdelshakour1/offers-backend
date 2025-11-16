from typing import List
from datetime import date

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.deps import require_superadmin
from app.db.session import get_db
from app.models.activities import Activity
from app.schemas.activities import ActivityOut
from app.services.storage import save_upload

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("/", response_model=ActivityOut, dependencies=[Depends(require_superadmin)])
async def create_activity(
    headline: str = Form(...),
    description: str | None = Form(None),
    link: str | None = Form(None),
    date: date | None = Form(None),
    order_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = save_upload(image, subdir="images") if image else None
    item = Activity(headline=headline, description=description, image_url=image_url, date=date, link=link, order_id=order_id)
    db.add(item)
    try:
        db.commit()
        db.refresh(item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order ID {order_id} already exists"
        )
    return {
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "link": item.link,
        "image_url": item.image_url,
        "order_id": item.order_id
    }


@router.get("/", response_model=List[ActivityOut])
async def list_activities(db: Session = Depends(get_db)):
    items = db.query(Activity).order_by(Activity.order_id.desc().nullslast(), Activity.id.desc()).all()
    return [{
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "link": item.link,
        "image_url": item.image_url,
        "order_id": item.order_id
    } for item in items]


@router.get("/{item_id}", response_model=ActivityOut)
async def get_activity(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Activity, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return {
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "link": item.link,
        "image_url": item.image_url,
        "order_id": item.order_id
    }


@router.put("/{item_id}", response_model=ActivityOut, dependencies=[Depends(require_superadmin)])
async def update_activity(
    item_id: int,
    headline: str | None = Form(None),
    description: str | None = Form(None),
    link: str | None = Form(None),
    date_value: date | None = Form(None, alias="date"),
    order_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    item = db.get(Activity, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if headline is not None:
        item.headline = headline
    if description is not None:
        item.description = description
    if link is not None:
        item.link = link
    if date_value is not None:
        item.date = date_value
    if order_id is not None:
        item.order_id = order_id
    if image is not None:
        item.image_url = save_upload(image, subdir="images")

    try:
        db.commit()
        db.refresh(item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order ID {order_id} already exists"
        )
    return {
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "link": item.link,
        "image_url": item.image_url,
        "order_id": item.order_id
    }


@router.delete("/{item_id}", dependencies=[Depends(require_superadmin)])
async def delete_activity(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Activity, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(item)
    db.commit()
    return {"status": "deleted"}

