from sqlalchemy import Column, Integer, String, Float

from app.db.session import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    discount = Column(Float, nullable=True)
    parent_link = Column(String, nullable=True)
    child_link = Column(String, nullable=True)
    order_id = Column(Integer, nullable=True, index=True)
