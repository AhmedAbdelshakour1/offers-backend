import os
import uuid
from typing import Optional

from fastapi import UploadFile

from app.core.config import settings


def save_upload(file: UploadFile, subdir: str = "") -> Optional[str]:
    if not file:
        return None
    safe_subdir = subdir.strip().strip("/")
    target_dir = os.path.join(settings.UPLOAD_DIR, safe_subdir) if safe_subdir else settings.UPLOAD_DIR
    os.makedirs(target_dir, exist_ok=True)

    ext = os.path.splitext(file.filename or "")[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    target_path = os.path.join(target_dir, filename)

    with open(target_path, "wb") as out:
        out.write(file.file.read())

    url_path = f"/uploads/{safe_subdir}/{filename}" if safe_subdir else f"/uploads/{filename}"
    return settings.BASE_URL.rstrip("/") + url_path
