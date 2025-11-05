from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.session import Base


class KeepInTouch(Base):
    __tablename__ = "keep_in_touch"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    mobile_number = Column(String(64), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
