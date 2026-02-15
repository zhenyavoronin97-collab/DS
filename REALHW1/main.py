import pandas as pd
import numpy as np
from data_loader import DataLoader
from data_processing import DataProcessor

# 1. Загружаем данные из CSV (файл spotify_hits.csv должен лежать в папке)
loader = DataLoader()
df = loader.load_csv('spotify_long_tracks_2014_2024.csv', encoding='utf-8')  # при необходимости измените кодировку

print("\nПервые 5 строк датасета Spotify:")
print(df.head())

# 2. Создаём процессор
proc = DataProcessor(df)

# 3. Анализ пропущенных значений
print("\n" + "="*50)
print("АНАЛИЗ ПРОПУЩЕННЫХ ЗНАЧЕНИЙ")
print("="*50)
report = proc.missing_values_report()

# 4. Заполнение пропусков
print("\n" + "="*50)
print("ЗАПОЛНЕНИЕ ПРОПУСКОВ")
print("="*50)

# Заполняем числовые столбцы средним
numeric_cols = proc.df.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_cols:
    if proc.df[col].isnull().any():
        proc.fill_missing(col, method='mean')

# Заполняем категориальные столбцы модой (самым частым значением)
cat_cols = proc.df.select_dtypes(include=['object']).columns.tolist()
for col in cat_cols:
    if proc.df[col].isnull().any():
        proc.fill_missing(col, method='mode')

print("\nПосле заполнения пропусков:")
print(proc.missing_values_count())

# 5. Визуализация
print("\n" + "="*50)
print("ВИЗУАЛИЗАЦИЯ ДАННЫХ")
print("="*50)

# 5.1 Гистограмма популярности треков
if 'popularity' in proc.df.columns:
    proc.add_histogram('popularity', bins=20, color='green', edgecolor='black', alpha=0.7)

# 5.2 Гистограмма энергии
if 'energy' in proc.df.columns:
    proc.add_histogram('energy', bins=20, color='orange', edgecolor='black', alpha=0.7)

# 5.3 Линейный график: средняя популярность по годам
if 'year' in proc.df.columns and 'popularity' in proc.df.columns:
    # Группируем по году и считаем среднюю популярность
    yearly_pop = proc.df.groupby('year')['popularity'].mean().reset_index()
    # Создаём временный процессор для агрегированных данных
    agg_proc = DataProcessor(yearly_pop)
    agg_proc.add_lineplot(x='year', y='popularity', marker='o', linestyle='-', color='red')
    # Добавляем его график в основной список
    proc.plots.extend(agg_proc.plots)
    print("Линейный график средней популярности по годам добавлен.")

# 5.4 Диаграмма рассеяния: энергия vs танцевальность с окраской по году
if all(col in proc.df.columns for col in ['energy', 'danceability', 'year']):
    # Создаём категориальный признак года для наглядности (разбиваем на 5 интервалов)
    proc.df['year_cat'] = pd.cut(proc.df['year'], bins=5, labels=False)
    proc.add_scatter(x='energy', y='danceability', hue='year_cat', alpha=0.6, palette='viridis')
    # Удаляем временный столбец
    proc.df.drop('year_cat', axis=1, inplace=True)
else:
    if 'energy' in proc.df.columns and 'danceability' in proc.df.columns:
        proc.add_scatter(x='energy', y='danceability', alpha=0.5)

# Добавим ещё один график для демонстрации удаления
if 'tempo' in proc.df.columns:
    proc.add_histogram('tempo', bins=30, color='purple', alpha=0.5)

print(f"\nВсего графиков создано: {len(proc.plots)}")

# Удаляем последний график (tempo)
proc.remove_last_plot()
print(f"После удаления осталось графиков: {len(proc.plots)}")

# 6. Отображение всех графиков
print("\nОткрытие окон с графиками (закройте их для продолжения)...")
proc.show_all_plots()

# 7. Дополнительная информация
print("\n" + "="*50)
print("ТИПЫ ДАННЫХ И СТАТИСТИКА")
print("="*50)
print("\nТипы столбцов:")
print(proc.check_data_types())

print("\nСтатистическое описание:")
print(proc.summary_statistics())