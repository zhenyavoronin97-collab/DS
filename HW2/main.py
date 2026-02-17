"""
Основной модуль проекта.
Загружает данные, обрабатывает и строит визуализации.
"""
import logging
from data_loader import load_data
from data_processer import clean_data, aggregate_sales_by_category, filter_by_date
from visualisation import plot_sales_by_category, plot_profit_vs_sales_scatter, plot_sales_timeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_FILE = "sales_data.csv"


def main():
    """Главная функция выполнения анализа."""
    logging.info("Запуск анализа данных.")

    # 1. Загрузка
    df = load_data(DATA_FILE)

    # 2. Очистка
    df_clean = clean_data(df)

    # 3. Фильтрация по дате (например, последний квартал 2023)
    df_filtered = filter_by_date(df_clean, '2023-10-01', '2023-12-31')

    # 4. Агрегация по категориям
    category_stats = aggregate_sales_by_category(df_filtered)

    # 5. Визуализации
    plot_sales_by_category(category_stats, top_n=10)
    plot_profit_vs_sales_scatter(df_filtered)
    plot_sales_timeline(df_filtered)

    logging.info("Анализ завершён.")


if __name__ == "__main__":
    main()