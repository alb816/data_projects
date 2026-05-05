from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime


# ORM - object-relational mapping (объектно-реляционное отображение). f: classes -> tables

Base = declarative_base() # создает базовый класс для определения моделей (классов, описывающих структуру таблиц баз данных)

# Модель таблицы
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)
    book_url = Column(String(500), unique=True, nullable=False)
    parsed_at = Column(DateTime, default=datetime.utcnow)