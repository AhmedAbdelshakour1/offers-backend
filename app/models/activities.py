from sqlalchemy import Column, Integer, String, Date

from app.db.session import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    link = Column(String, nullable=True)
    order_id = Column(Integer, nullable=True, index=True)
