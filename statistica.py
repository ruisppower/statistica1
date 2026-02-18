import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Показать все столбцы без сокращений
pd.set_option('display.max_columns', None)

# Если текст в столбцах обрезается
pd.set_option('display.max_colwidth', None)

# Показать все строки (если нужно)
pd.set_option('display.max_rows', None)


df = pd.read_csv(r'...............')

print(df.head())

# Размер данных (строки, столбцы)
print(f"Размер данных: {df.shape}")

# Названия столбцов
print(f"Столбцы: {df.columns.tolist()}")

# Информация о данных (типы, количество не-null значений)
print(df.info())

# Типы данных каждого столбца
print(f"Типы данных:\n{df.dtypes}")

# Проверка пропущенных значений
print(f"Пропущенные значения:\n{df.isnull().sum()}")

# Если есть пропуски - удалить
df = df.dropna()

# Проверить, что пропуски удалены
print(f"Пропущенные значения после удаления:\n{df.isnull().sum()}")

# 1. Описательные характеристики Year
print("Описательные характеристики переменной Year:")
print(df['Year'].describe())

# 2. График распределения количества игр по годам
# Считаем количество игр для каждого года
games_per_year = df['Year'].value_counts().sort_index()

# Строим график
plt.figure(figsize=(12, 6))
games_per_year.plot(kind='bar')
# или можно сделать линейный график: games_per_year.plot(kind='line')

plt.xlabel('Year')
plt.ylabel('Number of Games')
plt.title('Distribution of Games Released by Year')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Подсчет количества релизов по платформам
platform_counts = df['Platform'].value_counts()

# Вывести топ-10 платформ с наибольшим количеством релизов
print("Топ-10 платформ по количеству релизов:")
print(platform_counts.head(10))

# Или вывести все платформы
print("\nВсе платформы:")
print(platform_counts)

# Визуализация топ-10
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
platform_counts.head(10).plot(kind='bar')
plt.title('Топ-10 платформ по количеству релизов')
plt.xlabel('Platform')
plt.ylabel('Number of Games')
plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()


# Подсчет количества игр по издателям
publisher_counts = df['Publisher'].value_counts()

# Вывести топ-10 издателей с наибольшим количеством игр
print("Топ-10 издателей по количеству игр в датасете:")
print(publisher_counts.head(10))


# 1. Отфильтровать игры Nintendo
nintendo_games = df[df['Publisher'] == 'Nintendo']

# 2. Посчитать медиану продаж по каждому региону
na_median = nintendo_games['NA_Sales'].median()
eu_median = nintendo_games['EU_Sales'].median()
jp_median = nintendo_games['JP_Sales'].median()
other_median = nintendo_games['Other_Sales'].median()

# 3. Вывести результаты
print("Медианные продажи игр Nintendo по регионам:")
print(f"NA_Sales (Северная Америка): {na_median:.2f} млн")
print(f"EU_Sales (Европа): {eu_median:.2f} млн")
print(f"JP_Sales (Япония): {jp_median:.2f} млн")
print(f"Other_Sales (другие регионы): {other_median:.2f} млн")

# 4. Определить регион с наибольшей медианой
medians = {
    'NA': na_median,
    'EU': eu_median,
    'JP': jp_median,
    'Other': other_median
}

max_region = max(medians, key=medians.get)
max_value = medians[max_region]

print(f"\nРегион с наибольшей медианой продаж: {max_region} ({max_value:.2f} млн)")



# 1. Отфильтровать игры Nintendo
nintendo_games = df[df['Publisher'] == 'Nintendo']

# 2. Сгруппировать по жанрам и посчитать статистику по JP_Sales
genre_stats = nintendo_games.groupby('Genre')['JP_Sales'].agg([
    ('median', 'median'),
    ('mean', 'mean'),
    ('std', 'std'),
    ('min', 'min'),
    ('max', 'max'),
    ('count', 'count'),
    ('q1', lambda x: x.quantile(0.25)),
    ('q3', lambda x: x.quantile(0.75))
])

# Межквартильный размах (IQR) = Q3 - Q1
genre_stats['iqr'] = genre_stats['q3'] - genre_stats['q1']

# Округлить для удобства
genre_stats = genre_stats.round(2)

print("Статистика продаж игр Nintendo в Японии по жанрам:")
print(genre_stats.sort_values('median', ascending=False))




# 7. Визуализация динамики мировых продаж игр Nintendo по годам для выбранных жанров

# 1. Отфильтровать игры Nintendo нужных жанров
selected_genres = ['Fighting', 'Simulation', 'Platform', 'Racing', 'Sports']
nintendo_filtered = df[(df['Publisher'] == 'Nintendo') &
                       (df['Genre'].isin(selected_genres))]

# 2. Сгруппировать по году и жанру, суммировать продажи
yearly_sales = nintendo_filtered.groupby(['Year', 'Genre'])['Global_Sales'].sum().reset_index()

# 3. Создать сводную таблицу для удобного построения графиков
pivot_sales = yearly_sales.pivot(index='Year', columns='Genre', values='Global_Sales').fillna(0)

# 4. Построить график динамики продаж
plt.figure(figsize=(14, 7))

for genre in selected_genres:
    if genre in pivot_sales.columns:
        plt.plot(pivot_sales.index, pivot_sales[genre], marker='o', linewidth=2, markersize=4, label=genre)

plt.title('Динамика мировых продаж игр Nintendo по жанрам', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Мировые продажи (млн)', fontsize=12)
plt.legend(title='Жанр')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 5. Анализ для жанра Sports - в какие моменты продано больше всего?
sports_sales = nintendo_filtered[nintendo_filtered['Genre'] == 'Sports'].groupby('Year')['Global_Sales'].sum()

print("\n" + "="*60)
print("АНАЛИЗ ПРОДАЖ ИГР NINTENDO ЖАНРА SPORTS")
print("="*60)

print("\nПродажи игр Nintendo жанра Sports по годам:")
print(sports_sales.sort_values(ascending=False).round(2))

# Год с максимальными продажами
max_year = sports_sales.idxmax()
max_sales = sports_sales.max()
print(f"\n БОЛЬШЕ ВСЕГО игр жанра Sports было продано в {max_year} году: {max_sales:.2f} млн копий")

# Топ-3 года по продажам Sports
print("\n Топ-3 года с наибольшими продажами игр жанра Sports:")
top3_years = sports_sales.nlargest(3)
for year, sales in top3_years.items():
    print(f"   {year}: {sales:.2f} млн")

# 6. Детальный график для Sports
plt.figure(figsize=(12, 6))
sports_sales.sort_index().plot(kind='bar', color='orange', edgecolor='black', linewidth=0.5)
plt.title('Мировые продажи игр Nintendo жанра Sports по годам', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Продажи (млн)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')

# Подсветка максимального года
max_index = list(sports_sales.sort_index().index).index(max_year)
plt.gca().patches[max_index].set_color('red')
plt.gca().patches[max_index].set_alpha(0.8)

plt.tight_layout()
plt.show()

# 7. Дополнительно: топ-5 игр Sports по продажам
print("\n Топ-5 игр Nintendo жанра Sports по мировым продажам:")
top5_sports_games = nintendo_filtered[nintendo_filtered['Genre'] == 'Sports'].nlargest(5, 'Global_Sales')[['Name', 'Year', 'Global_Sales']]
for idx, row in top5_sports_games.iterrows():
    print(f"   {row['Name']} ({row['Year']}): {row['Global_Sales']:.2f} млн")



