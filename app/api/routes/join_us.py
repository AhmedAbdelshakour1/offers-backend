from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.api.deps import require_superadmin
from app.db.session import get_db
from app.models.join_us import JoinUs
from app.schemas.join_us import JoinUsOut
from app.services.storage import save_upload

router = APIRouter(prefix="/join-us", tags=["join-us"])


@router.post("/", response_model=JoinUsOut)
async def submit_join_us(
    name: str = Form(...),
    mobile_number: str | None = Form(None),
    email: str | None = Form(None),
    cv: UploadFile | None = File(None),
    job_role: str | None = Form(None),
    db: Session = Depends(get_db),
):
    cv_url = save_upload(cv, subdir="cv") if cv else None
    item = JoinUs(name=name, mobile_number=mobile_number, email=email, cv_url=cv_url, job_role=job_role)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=List[JoinUsOut], dependencies=[Depends(require_superadmin)])
async def list_join_us(db: Session = Depends(get_db)):
    return db.query(JoinUs).order_by(JoinUs.id.desc()).all()
