import os
import re
import json

# Папки ввода и вывода
input_folder = "2"  # Замените на путь к папке с HTML
output_folder = "задание2"
os.makedirs(output_folder, exist_ok=True)

# Функция для парсинга одного продукта
def parse_product(product_html):
    product = {}

    # Извлечение ID
    id_match = re.search(r'data-id="(\d+)"', product_html)
    if id_match:
        product["ID"] = id_match.group(1)

    # Извлечение Названия, Диагонали и Объема памяти
    title_match = re.search(r'<span>\s*(.+?)\s*</span>', product_html, re.DOTALL)
    if title_match:
        full_title = title_match.group(1).strip()
        diag_match = re.search(r'(\d+(\.\d+)?)"', full_title)  # Диагональ
        memory_match = re.search(r'(\d+)\s*GB', full_title)  # Объем памяти
        name_match = re.search(r'"\s*(.*?)\s*\d+\s*GB', full_title)  # Название устройства

        product["Полное название"] = full_title
        product["Диагональ"] = float(diag_match.group(1)) if diag_match else None
        product["Название"] = name_match.group(1).strip() if name_match else "Не указано"
        product["Объем памяти"] = int(memory_match.group(1)) if memory_match else None

    # Извлечение Цены
    price_match = re.search(r'<price>\s*([\d\s]+) ₽\s*</price>', product_html)
    if price_match:
        product["Цена"] = int(price_match.group(1).replace(" ", ""))

    # Извлечение характеристик
    spec_matches = re.findall(r'<li type="(.+?)">\s*(.+?)\s*</li>', product_html)
    if spec_matches:
        for spec_type, spec_value in spec_matches:
            product[spec_type.capitalize()] = spec_value.strip()

    return product

# Чтение и обработка всех HTML файлов
all_products = []
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        with open(os.path.join(input_folder, file_name), "r", encoding="utf-8") as file:
            content = file.read()
            # Разделяем на блоки продуктов
            product_blocks = re.findall(r'<div class="product-item">.*?</div>\s*</div>', content, re.DOTALL)
            for block in product_blocks:
                parsed_product = parse_product(block)
                # Проверяем, есть ли у продукта валидные данные
                if parsed_product.get("Цена") is not None:
                    all_products.append(parsed_product)

# Сохранение всех продуктов в JSON
output_path = os.path.join(output_folder, "products.json")
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=4)

# Операции
# 1. Сортировка по цене
sorted_products = sorted(all_products, key=lambda x: x.get("Цена", 0))

# Сохранение отсортированных продуктов
sorted_path = os.path.join(output_folder, "sorted_products.json")
with open(sorted_path, "w", encoding="utf-8") as file:
    json.dump(sorted_products, file, ensure_ascii=False, indent=4)

# 2. Фильтрация по RAM > 8GB
filtered_products = [p for p in all_products if int(p.get("Ram", "0 GB").split()[0]) > 8]

# Сохранение отфильтрованных продуктов
filtered_path = os.path.join(output_folder, "filtered_products.json")
with open(filtered_path, "w", encoding="utf-8") as file:
    json.dump(filtered_products, file, ensure_ascii=False, indent=4)

# 3. Статистические характеристики по цене
prices = [p["Цена"] for p in all_products if "Цена" in p]
price_stats = {
    "Сумма": sum(prices),
    "Минимум": min(prices),
    "Максимум": max(prices),
    "Среднее": round(sum(prices) / len(prices), 2) if prices else 0,
    "Количество записей": len(prices)
}

# Сохранение статистики по ценам
stats_path = os.path.join(output_folder, "price_stats.json")
with open(stats_path, "w", encoding="utf-8") as file:
    json.dump(price_stats, file, ensure_ascii=False, indent=4)

# 4. Частота типов матриц
matrix_counts = {}
for p in all_products:
    matrix = p.get("Matrix", None)
    if matrix:
        matrix_counts[matrix] = matrix_counts.get(matrix, 0) + 1

# Сохранение частоты типов матриц
matrix_counts_path = os.path.join(output_folder, "matrix_counts.json")
with open(matrix_counts_path, "w", encoding="utf-8") as file:
    json.dump(matrix_counts, file, ensure_ascii=False, indent=4)