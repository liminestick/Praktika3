import os
import json
import re

# Папки ввода и вывода
input_folder = "1"
output_folder = "задание1"  # Папка для сохранения результатов

# Регулярные выражения для извлечения данных
patterns = {
    "Артикул": r"Артикул:\s*([\w-]+)(?=\s*Наличие:)",  # Артикул и Наличие разделяются
    "Наличие": r"Наличие:\s*(Да|Нет)",
    "Название": r"Название:\s*([\w\s]+)",
    "Город": r"Город:\s*([\w\s]+?)(?=Цена:)",  # Город до слова "Цена"
    "Цена": r"Цена:\s*(\d+)\s*руб",
    "Цвет": r"Цвет:\s*([\w\s]+)",
    "Количество": r"Количество:\s*(\d+)\s*шт",
    "Размеры": r"Размеры:\s*([\dx]+)",
}


# Функция для парсинга текста из HTML-файлов
def parse_html_as_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        product = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.DOTALL)
            if match:
                value = match.group(1).strip()
                if key in ["Цена", "Количество"]:
                    value = int(value)
                product[key] = value

        # Проверяем наличие Артикул и Наличие
        if "Артикул" not in product:
            product["Артикул"] = "Не указан"
        if "Наличие" not in product:
            product["Наличие"] = "Не указано"

        return product


# Чтение всех файлов и парсинг
data = []
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        file_path = os.path.join(input_folder, file_name)
        data.append(parse_html_as_text(file_path))

# Сохранение данных в JSON
output_json_path = os.path.join(output_folder, "products.json")
with open(output_json_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Операции с данными

# 1. Сортировка по цене
sorted_data = sorted(data, key=lambda x: x.get("Цена", 0))

# Сохранение отсортированных данных
with open(os.path.join(output_folder, "sorted.json"), "w", encoding="utf-8") as file:
    json.dump(sorted_data, file, ensure_ascii=False, indent=4)

# 2. Фильтрация по количеству больше 500
filtered_data = [item for item in data if item.get("Количество", 0) > 500]

# Сохранение отфильтрованных данных
with open(os.path.join(output_folder, "filtered.json"), "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)

# 3. Статистические характеристики по полю "Цена"
prices = [item["Цена"] for item in data if "Цена" in item]
stats = {
    "Сумма": sum(prices),
    "Минимум": min(prices),
    "Максимум": max(prices),
    "Среднее": sum(prices) / len(prices) if prices else 0,
    "Количество записей": len(prices),
}

# Сохранение статистики
with open(os.path.join(output_folder, "stats.json"), "w", encoding="utf-8") as file:
    json.dump(stats, file, ensure_ascii=False, indent=4)

# 4. Частота значений по полю "Цвет"
color_counts = {}
for item in data:
    color = item.get("Цвет", "Не указан")
    if color not in color_counts:
        color_counts[color] = 0
    color_counts[color] += 1

# Сохранение частоты значений
with open(os.path.join(output_folder, "color_counts.json"), "w", encoding="utf-8") as file:
    json.dump(color_counts, file, ensure_ascii=False, indent=4)
