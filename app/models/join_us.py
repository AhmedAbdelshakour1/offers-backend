from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.session import Base


class JoinUs(Base):
    __tablename__ = "join_us"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    mobile_number = Column(String(64), nullable=True)
    email = Column(String(255), nullable=True)
    cv_url = Column(String, nullable=True)
    job_role = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
