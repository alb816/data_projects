from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base() # базовый класс для определения модели


class PremiumBook(Base):
    __tablename__ = 'premium_books'
    id = Column(Integer, primary_key=True)
    book_url = Column(String(500), unique=False, nullable=False)
    title = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    image_link = Column(Text)
    parsed_at = Column(DateTime, default=datetime.utcnow)