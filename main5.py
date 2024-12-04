import os
import json

# Данные о продуктах (предположим, это результат предыдущего парсинга)
products = [
    {
        "Название": "PORGELAIN ETCHANT 9.5%",
        "Описание": "Протравка для фарфора с 9,5% буферной плавиковой кислоты.",
        "Цена": 1250,
        "Единица измерения": "уп",
        "Наличие": "да"
    },
    {
        "Название": "Адгезив DiaPlus, DiaDent",
        "Описание": "Однокомпонентное вещество с высокой силой сцепления.",
        "Цена": 789,
        "Единица измерения": "шт",
        "Наличие": "да"
    },
    {
        "Название": "Adhesive UNI Bond",
        "Описание": "Универсальный адгезив для стоматологических реставраций.",
        "Цена": 2300,
        "Единица измерения": "шт",
        "Наличие": "нет"
    },
    {
        "Название": "Adhesive Clearfil",
        "Описание": "Эффективен для работы с керамическими материалами.",
        "Цена": 1141,
        "Единица измерения": "шт",
        "Наличие": "да"
    }
]

# Создание папки для результатов
output_folder = "задание5"
os.makedirs(output_folder, exist_ok=True)

# 1. Сортировка по цене
sorted_products = sorted(products, key=lambda x: x['Цена'] if x['Цена'] else 0)
with open(os.path.join(output_folder, "sorted_products.json"), "w", encoding="utf-8") as file:
    json.dump(sorted_products, file, ensure_ascii=False, indent=4)

# 2. Фильтрация по наличию
filtered_products = [product for product in products if product['Наличие'] == 'да']
with open(os.path.join(output_folder, "filtered_products.json"), "w", encoding="utf-8") as file:
    json.dump(filtered_products, file, ensure_ascii=False, indent=4)

# 3. Статистика по цене
prices = [product['Цена'] for product in products if product['Цена']]
price_stats = {
    "Сумма": sum(prices),
    "Минимум": min(prices),
    "Максимум": max(prices),
    "Среднее": sum(prices) / len(prices) if prices else 0,
    "Количество записей": len(prices)
}
with open(os.path.join(output_folder, "price_stats.json"), "w", encoding="utf-8") as file:
    json.dump(price_stats, file, ensure_ascii=False, indent=4)

# 4. Частота меток по единицам измерения
unit_counts = {}
for product in products:
    unit = product['Единица измерения']
    if unit:
        unit_counts[unit] = unit_counts.get(unit, 0) + 1

with open(os.path.join(output_folder, "unit_counts.json"), "w", encoding="utf-8") as file:
    json.dump(unit_counts, file, ensure_ascii=False, indent=4)

print(f"Результаты сохранены в папку: {output_folder}")
