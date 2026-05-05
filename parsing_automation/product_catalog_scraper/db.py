from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Установка соединения с базой данных
engine = create_engine (
    db_url,
    echo=False # echo=False отключает вывод всех SQL-запросов в консоль
) 

# Создание сессии, в контексте которой будут происходить все SQL-запросы
session = sessionmaker(bind=engine) # bind=engine связывает сессию с нашим движком базы данных