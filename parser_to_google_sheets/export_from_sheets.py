import pandas as pd
from gspread.auth import service_account
from config import SHEET
import logging


def client_init_json():
    return service_account(filename='credentials.json')


def export_from_sheets(output_file="tables/data.csv", sheet_name=SHEET):
    try:
        # подключаемся к Google Sheets
        client = client_init_json()
        sheet = client.open(sheet_name).sheet1

        # получаем все данные
        data = sheet.get_all_records()

        if not data:
            logging.warning("Таблица пустая!")
            return

        # превращаем в DataFrame
        df = pd.DataFrame(data)
        df.drop_duplicates(inplace=True)
        
        # сохраняем в CSV
        df.to_csv(output_file, index=False)

    except Exception as e:
        logging.error(f"Ошибка при выгрузке из Google Sheets: {e}")
    