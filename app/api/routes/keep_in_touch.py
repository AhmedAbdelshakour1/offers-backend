from typing import List

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.api.deps import require_superadmin
from app.db.session import get_db
from app.models.keep_in_touch import KeepInTouch
from app.schemas.keep_in_touch import KeepInTouchOut

router = APIRouter(prefix="/keep-in-touch", tags=["keep-in-touch"])


@router.post("/", response_model=KeepInTouchOut)
async def submit_keep_in_touch(
    name: str = Form(...),
    mobile_number: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    item = KeepInTouch(name=name, mobile_number=mobile_number, email=email)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=List[KeepInTouchOut], dependencies=[Depends(require_superadmin)])
async def list_keep_in_touch(db: Session = Depends(get_db)):
    return db.query(KeepInTouch).order_by(KeepInTouch.id.desc()).all()
