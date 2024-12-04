import os
import json
import xml.etree.ElementTree as ET

# Папки ввода и вывода
input_folder = "4"
output_folder = "задание4"
os.makedirs(output_folder, exist_ok=True)


# Чтение данных из XML-файлов
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    products = []

    for clothing in root.findall('clothing'):
        product = {}
        for child in clothing:
            tag = child.tag
            text = child.text.strip() if child.text else None
            if tag == "price" or tag == "rating" or tag == "reviews":
                text = float(text) if "." in text else int(text)
            product[tag] = text
        products.append(product)
    return products


# Обработка всех XML-файлов
all_products = []
for file_name in os.listdir(input_folder):
    if file_name.endswith(".xml"):
        file_path = os.path.join(input_folder, file_name)
        all_products.extend(parse_xml(file_path))

# Сохранение данных в JSON
output_file = os.path.join(output_folder, "products.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)

# Сортировка по полю "price"
sorted_products = sorted(all_products, key=lambda x: x.get("price", 0))
sorted_file = os.path.join(output_folder, "sorted.json")
with open(sorted_file, "w", encoding="utf-8") as f:
    json.dump(sorted_products, f, ensure_ascii=False, indent=4)

# Фильтрация по цвету "Оранжевый"
filtered_products = [p for p in all_products if p.get("color") == "Оранжевый"]
filtered_file = os.path.join(output_folder, "filtered.json")
with open(filtered_file, "w", encoding="utf-8") as f:
    json.dump(filtered_products, f, ensure_ascii=False, indent=4)

# Статистика по полю "price"
prices = [p["price"] for p in all_products if "price" in p]
price_stats = {
    "Сумма": sum(prices),
    "Минимум": min(prices),
    "Максимум": max(prices),
    "Среднее": sum(prices) / len(prices),
    "Количество записей": len(prices),
}
stats_file = os.path.join(output_folder, "stats.json")
with open(stats_file, "w", encoding="utf-8") as f:
    json.dump(price_stats, f, ensure_ascii=False, indent=4)

# Частота меток по полю "color"
color_counts = {}
for p in all_products:
    color = p.get("color")
    if color:
        color_counts[color] = color_counts.get(color, 0) + 1
color_counts_file = os.path.join(output_folder, "color_counts.json")
with open(color_counts_file, "w", encoding="utf-8") as f:
    json.dump(color_counts, f, ensure_ascii=False, indent=4)
