
"""
Модуль загрузки данных из CSV-файла.
Содержит функцию load_data, которая читает файл и возвращает DataFrame.
"""
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, parse_dates=['date'])
        logging.info(f"Данные успешно загружены из {file_path}. Размер: {df.shape}")
        return df
    except FileNotFoundError:
        logging.error(f"Файл не найден: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logging.error(f"Файл пуст: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {e}")
        raise

if __name__ == "__main__":
    data = load_data("sales_data.csv")
    print(data.head())