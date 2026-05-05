from gspread.auth import service_account
from config import SHEET
import logging


def client_init_json():
    return service_account(filename='credentials.json')

def upload_to_sheets(data, sheet_name= SHEET):
    if not data:
        logging.warning("Отсутствуют данные для загрузки!")

    try:
        # Инициализируем клиента и открываем таблицу
        client = client_init_json()
        sheet = client.open(sheet_name).sheet1
        sheet.clear()
        
        # Создание столбцов и строк таблицы      
        headers = list(data[0].keys())
        rows = [headers] + [list(item.values()) for item in data]
        sheet.update(rows)
    except Exception as e:
        logging.error(f"Ошибка при загрузке в Google Sheets: {e}")
