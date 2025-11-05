from typing import List
from datetime import date

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_superadmin
from app.db.session import get_db
from app.models.news import News
from app.schemas.news import NewsOut
from app.services.storage import save_upload

router = APIRouter(prefix="/news", tags=["news"], dependencies=[Depends(require_superadmin)])


@router.post("/", response_model=NewsOut)
async def create_news(
    headline: str = Form(...),
    description: str | None = Form(None),
    date_value: date | None = Form(None, alias="date"),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = save_upload(image, subdir="images") if image else None
    item = News(headline=headline, description=description, image_url=image_url, date=date_value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "image_url": item.image_url
    }


@router.get("/", response_model=List[NewsOut])
async def list_news(db: Session = Depends(get_db)):
    items = db.query(News).order_by(News.id.desc()).all()
    return [{
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "image_url": item.image_url
    } for item in items]


@router.get("/{item_id}", response_model=NewsOut)
async def get_news(item_id: int, db: Session = Depends(get_db)):
    item = db.get(News, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return {
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "image_url": item.image_url
    }


@router.put("/{item_id}", response_model=NewsOut)
async def update_news(
    item_id: int,
    headline: str | None = Form(None),
    description: str | None = Form(None),
    date_value: date | None = Form(None, alias="date"),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    item = db.get(News, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if headline is not None:
        item.headline = headline
    if description is not None:
        item.description = description
    if date_value is not None:
        item.date = date_value
    if image is not None:
        item.image_url = save_upload(image, subdir="images")

    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "headline": item.headline,
        "description": item.description,
        "date": item.date.isoformat() if item.date else None,
        "image_url": item.image_url
    }


@router.delete("/{item_id}")
async def delete_news(item_id: int, db: Session = Depends(get_db)):
    item = db.get(News, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(item)
    db.commit()
    return {"status": "deleted"}

