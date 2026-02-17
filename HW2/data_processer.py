"""
Модуль обработки и агрегации данных.
Содержит функции для очистки, фильтрации и группировки данных.
"""
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очищает данные: удаляет дубликаты, пропуски и приводит типы.

    Параметры:
        df (pd.DataFrame): исходный DataFrame.

    Возвращает:
        pd.DataFrame: очищенный DataFrame.
    """
    initial_shape = df.shape
    # Удаление дубликатов
    df = df.drop_duplicates()
    # Удаление строк с пропущенными значениями
    df = df.dropna()
    # Приведение sales и profit к числовому типу (если ещё не числа)
    for col in ['sales', 'profit']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # После преобразования снова удаляем строки с NaN (если появились)
    df = df.dropna(subset=['sales', 'profit'])
    logging.info(f"Очистка данных: было {initial_shape}, стало {df.shape}")
    return df


def aggregate_sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Группирует данные по категориям, суммируя продажи и прибыль.

    Параметры:
        df (pd.DataFrame): очищенный DataFrame.

    Возвращает:
        pd.DataFrame: агрегированные данные.
    """
    grouped = df.groupby('category', as_index=False).agg({
        'sales': 'sum',
        'profit': 'sum'
    })
    grouped = grouped.sort_values('sales', ascending=False)
    logging.info(f"Агрегация по категориям выполнена. Категорий: {len(grouped)}")
    return grouped


def filter_by_date(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Фильтрует данные по диапазону дат.

    Параметры:
        df (pd.DataFrame): DataFrame с колонкой 'date' (datetime).
        start_date (str): начальная дата в формате YYYY-MM-DD.
        end_date (str): конечная дата в формате YYYY-MM-DD.

    Возвращает:
        pd.DataFrame: отфильтрованный DataFrame.
    """
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered = df.loc[mask]
    logging.info(f"Фильтр по датам: с {start_date} по {end_date}, осталось записей: {len(filtered)}")
    return filtered


if __name__ == "__main__":
    # Пример тестирования модуля
    sample_data = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-01'],
        'product': ['A', 'B', 'A'],
        'category': ['Electronics', 'Clothing', 'Electronics'],
        'sales': [100, 200, 150],
        'profit': [20, 30, 25]
    })
    sample_data['date'] = pd.to_datetime(sample_data['date'])
    cleaned = clean_data(sample_data)
    print("Очищенные данные:\n", cleaned)
    aggregated = aggregate_sales_by_category(cleaned)
    print("Агрегация по категориям:\n", aggregated)
    filtered = filter_by_date(cleaned, '2023-01-01', '2023-01-01')
    print("Фильтр по дате 2023-01-01:\n", filtered)