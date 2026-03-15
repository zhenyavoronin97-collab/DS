"""
Модуль визуализации данных.
Содержит функции для построения графиков на основе DataFrame.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def plot_sales_by_category(df: pd.DataFrame, top_n: int = 10) -> None:
    """
    Строит столбчатую диаграмму продаж по категориям (топ-N).
    """
    df_sorted = df.sort_values('sales', ascending=False).head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_sorted, x='sales', y='category', 
                hue='category', palette='viridis', legend=False)
    plt.title(f'Топ-{top_n} категорий по объёму продаж')
    plt.xlabel('Суммарные продажи')
    plt.ylabel('Категория')
    plt.tight_layout()
    logging.info(f"Построен график продаж по категориям (топ-{top_n})")
    plt.show()


def plot_profit_vs_sales_scatter(df: pd.DataFrame) -> None:
    """
    Строит точечную диаграмму зависимости прибыли от продаж.

    Параметры:
        df (pd.DataFrame): исходный или агрегированный DataFrame с колонками 'sales' и 'profit'.
    """
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='sales', y='profit', hue='category' if 'category' in df.columns else None, alpha=0.7)
    plt.title('Зависимость прибыли от продаж')
    plt.xlabel('Продажи')
    plt.ylabel('Прибыль')
    plt.tight_layout()
    logging.info("Построен scatter plot прибыли от продаж")
    plt.show()


def plot_sales_timeline(df: pd.DataFrame) -> None:
    """
    Строит временной ряд суммарных продаж по дням.

    Параметры:
        df (pd.DataFrame): исходный DataFrame с колонками 'date' и 'sales'.
    """
    # Группировка по датам, суммирование продаж
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=daily_sales, x='date', y='sales', marker='o')
    plt.title('Динамика продаж по дням')
    plt.xlabel('Дата')
    plt.ylabel('Суммарные продажи')
    plt.xticks(rotation=45)
    plt.tight_layout()
    logging.info("Построен временной ряд продаж")
    plt.show()


if __name__ == "__main__":
    # Пример тестирования модуля
    sample_agg = pd.DataFrame({
        'category': ['Electronics', 'Clothing', 'Books', 'Home', 'Sports'],
        'sales': [1500, 1200, 800, 600, 400],
        'profit': [300, 240, 160, 120, 80]
    })
    plot_sales_by_category(sample_agg)
    plot_profit_vs_sales_scatter(sample_agg)

    sample_timeline = pd.DataFrame({
        'date': pd.date_range('2023-01-01', periods=10),
        'sales': [100, 150, 130, 170, 160, 200, 210, 190, 180, 220]
    })
    plot_sales_timeline(sample_timeline)