import pandas as pd
import requests
from typing import Optional, Dict, Any

class DataLoader:
    """Класс для загрузки данных из различных источников."""

    @staticmethod
    def load_csv(file_path: str, **kwargs) -> pd.DataFrame:
        """
        Загружает данные из CSV-файла.
        :param file_path: путь к файлу
        :param kwargs: дополнительные параметры для pd.read_csv
        :return: DataFrame
        """
        try:
            df = pd.read_csv(file_path, **kwargs)
            print(f"CSV-файл '{file_path}' успешно загружен. Размер: {df.shape}")
            return df
        except Exception as e:
            print(f"Ошибка при загрузке CSV: {e}")
            raise

    @staticmethod
    def load_json(file_path: str, **kwargs) -> pd.DataFrame:
        """
        Загружает данные из JSON-файла.
        :param file_path: путь к файлу
        :param kwargs: дополнительные параметры для pd.read_json
        :return: DataFrame
        """
        try:
            df = pd.read_json(file_path, **kwargs)
            print(f"JSON-файл '{file_path}' успешно загружен. Размер: {df.shape}")
            return df
        except Exception as e:
            print(f"Ошибка при загрузке JSON: {e}")
            raise

    @staticmethod
    def load_api(url: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Загружает данные из API (GET-запрос, ожидается JSON-ответ).
        :param url: endpoint API
        :param params: параметры запроса
        :return: DataFrame
        """
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.json_normalize(data)
            else:
                raise ValueError("Не удалось преобразовать ответ API в DataFrame")
            print(f"Данные из API '{url}' успешно загружены. Размер: {df.shape}")
            return df
        except Exception as e:
            print(f"Ошибка при загрузке из API: {e}")
            raise