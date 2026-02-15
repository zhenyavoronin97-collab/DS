%%writefile data_processing.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List

class DataProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.plots = []

    # Пропуски
    def missing_values_count(self) -> pd.Series:
        return self.df.isnull().sum()

    def missing_values_report(self) -> pd.DataFrame:
        missing_count = self.missing_values_count()
        missing_percent = (missing_count / len(self.df)) * 100
        report = pd.DataFrame({
            'Количество пропусков': missing_count,
            'Доля пропусков (%)': missing_percent
        }).sort_values('Доля пропусков (%)', ascending=False)
        print("Отчёт о пропущенных значениях:")
        print(report)
        return report

    def fill_missing(self, column: str, method: str = 'mean', **kwargs) -> None:
        if column not in self.df.columns:
            raise ValueError(f"Столбец '{column}' не найден")
        if method == 'mean':
            if not np.issubdtype(self.df[column].dtype, np.number):
                raise TypeError("Метод 'mean' применим только к числовым столбцам")
            fill_value = self.df[column].mean()
        elif method == 'median':
            if not np.issubdtype(self.df[column].dtype, np.number):
                raise TypeError("Метод 'median' применим только к числовым столбцам")
            fill_value = self.df[column].median()
        elif method == 'mode':
            mode_vals = self.df[column].mode(dropna=True)
            if len(mode_vals) == 0:
                raise ValueError(f"Нет моды для столбца '{column}'")
            fill_value = mode_vals[0]
        elif method == 'constant':
            if 'value' not in kwargs:
                raise ValueError("Для метода 'constant' необходимо указать параметр 'value'")
            fill_value = kwargs['value']
        else:
            raise ValueError("Метод должен быть 'mean', 'median', 'mode' или 'constant'")
        self.df[column].fillna(fill_value, inplace=True)
        print(f"Пропуски в столбце '{column}' заполнены методом '{method}' (значение: {fill_value})")

    # Визуализация
    def add_histogram(self, column: str, bins: int = 30, **kwargs) -> None:
        if column not in self.df.columns:
            raise ValueError(f"Столбец '{column}' не найден")
        if not np.issubdtype(self.df[column].dtype, np.number):
            raise TypeError("Гистограмма строится только для числовых столбцов")
        fig, ax = plt.subplots(figsize=(8, 5))
        self.df[column].hist(bins=bins, ax=ax, **kwargs)
        ax.set_title(f'Гистограмма: {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Частота')
        self.plots.append(fig)
        plt.close(fig)
        print(f"Гистограмма для столбца '{column}' добавлена в список.")

    def add_lineplot(self, x: str, y: str, **kwargs) -> None:
        for col in [x, y]:
            if col not in self.df.columns:
                raise ValueError(f"Столбец '{col}' не найден")
        if not np.issubdtype(self.df[x].dtype, np.number) or not np.issubdtype(self.df[y].dtype, np.number):
            raise TypeError("Линейный график требует числовые столбцы")
        fig, ax = plt.subplots(figsize=(8, 5))
        sorted_df = self.df.sort_values(by=x)
        ax.plot(sorted_df[x], sorted_df[y], **kwargs)
        ax.set_title(f'Линейный график: {y} от {x}')
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        self.plots.append(fig)
        plt.close(fig)
        print(f"Линейный график ({y} от {x}) добавлен в список.")

    def add_scatter(self, x: str, y: str, hue: Optional[str] = None, **kwargs) -> None:
        for col in [x, y]:
            if col not in self.df.columns:
                raise ValueError(f"Столбец '{col}' не найден")
        if not np.issubdtype(self.df[x].dtype, np.number) or not np.issubdtype(self.df[y].dtype, np.number):
            raise TypeError("Диаграмма рассеяния требует числовые столбцы")
        fig, ax = plt.subplots(figsize=(8, 5))
        if hue is not None:
            if hue not in self.df.columns:
                raise ValueError(f"Столбец '{hue}' не найден")
            sns.scatterplot(data=self.df, x=x, y=y, hue=hue, ax=ax, **kwargs)
        else:
            ax.scatter(self.df[x], self.df[y], **kwargs)
        ax.set_title(f'Диаграмма рассеяния: {y} от {x}')
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        self.plots.append(fig)
        plt.close(fig)
        print(f"Диаграмма рассеяния ({y} от {x}) добавлена в список.")

    def remove_last_plot(self) -> None:
        if self.plots:
            self.plots.pop()
            print(f"График удалён. Осталось графиков: {len(self.plots)}")
        else:
            print("Список графиков пуст, нечего удалять.")

    def show_all_plots(self) -> None:
        if not self.plots:
            print("Нет графиков для отображения.")
            return
        for fig in self.plots:
            fig.show()
        plt.show()

    def check_data_types(self) -> pd.Series:
        return self.df.dtypes

    def summary_statistics(self) -> pd.DataFrame:
        return self.df.describe(include='all')