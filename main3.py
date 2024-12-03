import os
import json
import xml.etree.ElementTree as ET

# Папки ввода и вывода
input_folder = "3"
output_folder = "задание3"
os.makedirs(output_folder, exist_ok=True)


# Функция для парсинга одного XML файла
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    star = {}
    star["Название"] = root.findtext("name", default="").strip()
    star["Созвездие"] = root.findtext("constellation", default="").strip()
    star["Спектральный класс"] = root.findtext("spectral-class", default="").strip()
    star["Радиус"] = int(root.findtext("radius", default="0").strip())
    star["Период вращения"] = root.findtext("rotation", default="").strip()
    star["Возраст"] = root.findtext("age", default="").strip()
    star["Расстояние"] = float(root.findtext("distance", default="0").strip().replace(" million km", ""))
    star["Абсолютная звездная величина"] = root.findtext("absolute-magnitude", default="").strip()

    return star


# Чтение всех файлов и сбор данных
all_stars = []
for file_name in os.listdir(input_folder):
    if file_name.endswith(".xml"):
        file_path = os.path.join(input_folder, file_name)
        star_data = parse_xml(file_path)
        all_stars.append(star_data)

# Сохранение данных в JSON
output_path = os.path.join(output_folder, "stars.json")
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(all_stars, json_file, ensure_ascii=False, indent=4)

# Операции с данными
# 1. Сортировка по радиусу
sorted_stars = sorted(all_stars, key=lambda x: x["Радиус"])

# 2. Фильтрация по созвездию "Рыбы"
filtered_stars = [star for star in all_stars if star["Созвездие"] == "Рыбы"]

# 3. Статистические характеристики по радиусу
radii = [star["Радиус"] for star in all_stars]
radius_stats = {
    "Сумма": sum(radii),
    "Минимум": min(radii),
    "Максимум": max(radii),
    "Среднее": round(sum(radii) / len(radii), 2) if radii else 0
}

# 4. Частота спектральных классов
spectral_class_counts = {}
for star in all_stars:
    spectral_class = star["Спектральный класс"]
    spectral_class_counts[spectral_class] = spectral_class_counts.get(spectral_class, 0) + 1

# Сохранение результатов
with open(os.path.join(output_folder, "sorted_stars.json"), "w", encoding="utf-8") as file:
    json.dump(sorted_stars, file, ensure_ascii=False, indent=4)

with open(os.path.join(output_folder, "filtered_stars.json"), "w", encoding="utf-8") as file:
    json.dump(filtered_stars, file, ensure_ascii=False, indent=4)

with open(os.path.join(output_folder, "radius_stats.json"), "w", encoding="utf-8") as file:
    json.dump(radius_stats, file, ensure_ascii=False, indent=4)

with open(os.path.join(output_folder, "spectral_class_counts.json"), "w", encoding="utf-8") as file:
    json.dump(spectral_class_counts, file, ensure_ascii=False, indent=4)

print(f"Данные успешно обработаны и сохранены в папку: {output_folder}")
