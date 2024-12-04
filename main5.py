import requests
from bs4 import BeautifulSoup
import json
import os


# Функция для скачивания страницы
def download_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.text
    except Exception as e:
        print(f"Ошибка при скачивании страницы: {e}")
        return None


# Функция для обработки главной страницы каталога
def scrape_catalog_page(catalog_url):
    html_content = download_page(catalog_url)
    if not html_content:
        print("Не удалось скачать главную страницу.")
        return [], []

    soup = BeautifulSoup(html_content, "html.parser")
    main_top_cars_items = soup.find_all("div", class_="main-top-cars__item")

    catalog_data = []  # Для данных из каталога
    product_links = []  # Для ссылок на карточки товаров

    if main_top_cars_items:
        for item in main_top_cars_items:
            try:
                # Извлекаем данные о товаре
                info_block = item.find("div", class_="cars-item-2__info")
                name = info_block.find("span", class_="cars-item-2__heading").text.strip()
                status = info_block.find("div", class_="cars-item-2__status").text.strip()

                # Извлекаем параметры
                params = {}
                param_elements = info_block.find_all("div", class_="cars-item-2__param")
                for param in param_elements:
                    label = param.find("div", class_="cars-item-2__param_label").text.strip()
                    value = param.find("div", class_="cars-item-2__param_value").text.strip()
                    params[label] = value

                # Извлекаем цену
                price_block = item.find("div", class_="cars-item-2-control__price")
                price_value = "Цена не найдена"
                if price_block:
                    price_data = price_block.get("data-price")
                    if price_data:
                        price_list = json.loads(price_data)
                        for price_info in price_list:
                            if price_info.get("days_min") == 30 and price_info.get("days_max") == 999:
                                price_value = price_info.get("price", "Цена не найдена")

                # Добавляем в каталог
                catalog_data.append({
                    "Название": name,
                    "Тип авто": status,
                    "Параметры": params,
                    "Цена (в рублях)": price_value,
                    "Единица измерения": "руб."
                })

                # Извлекаем ссылку на карточку товара
                link_tag = item.find("a", class_="cars-item-2__link")
                if link_tag and link_tag.get("href"):
                    link = link_tag["href"]
                    if not link.startswith("http"):
                        link = "https://ekb.arendacar.ru" + link
                    product_links.append(link)

            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")
    else:
        print("Не удалось найти элементы с классом 'main-top-cars__item'.")

    return catalog_data, product_links


# Функция для обработки карточки товара
def scrape_product_page(product_url):
    html_content = download_page(product_url)
    if not html_content:
        print(f"Не удалось скачать страницу товара: {product_url}")
        return None

    soup = BeautifulSoup(html_content, "html.parser")
    car_data = {}

    for strong_tag in soup.find_all("strong"):
        key = strong_tag.text.strip()  # Извлекаем текст внутри <strong>
        value = strong_tag.next_sibling  # Значение после </strong>
        if value and isinstance(value, str):
            value = value.replace(":", "").strip()  # Убираем двоеточие и пробелы
            car_data[key] = value

    return car_data


# Основная функция для объединения данных
def scrape_and_save_all(catalog_url, output_folder="задание5"):
    os.makedirs(output_folder, exist_ok=True)

    # Парсим главную страницу
    print("Скачивание главной страницы каталога...")
    catalog_data, product_links = scrape_catalog_page(catalog_url)

    # Сохраняем каталог в JSON
    catalog_output_path = os.path.join(output_folder, "catalog.json")
    with open(catalog_output_path, "w", encoding="utf-8") as file:
        json.dump(catalog_data, file, ensure_ascii=False, indent=4)
    print(f"Данные каталога сохранены в файл: {catalog_output_path}")

    # Парсим каждую карточку товара
    print("Скачивание карточек товаров...")
    all_product_data = []
    for product_url in product_links:
        print(f"Обработка карточки товара: {product_url}")
        product_data = scrape_product_page(product_url)
        if product_data:
            all_product_data.append(product_data)

    # Сохраняем карточки в JSON
    products_output_path = os.path.join(output_folder, "products.json")
    with open(products_output_path, "w", encoding="utf-8") as file:
        json.dump(all_product_data, file, ensure_ascii=False, indent=4)
    print(f"Данные карточек товаров сохранены в файл: {products_output_path}")


    # Задания

    # 1. Сортировка по году выпуска
    sorted_by_year = sorted(catalog_data, key=lambda x: x['Параметры'].get('Год выпуска', 0))
    sorted_year_path = os.path.join(output_folder, "catalog_sorted_by_year.json")
    with open(sorted_year_path, "w", encoding="utf-8") as file:
        json.dump(sorted_by_year, file, ensure_ascii=False, indent=4)
    print(f"Данные каталога, отсортированные по году выпуска, сохранены в файл: {sorted_year_path}")

    # 2. Фильтрация по приводу (полный)
    filtered_by_drive = [item for item in catalog_data if 'Привод' in item['Параметры'] and item['Параметры']['Привод'].lower() == 'полный']
    filtered_drive_path = os.path.join(output_folder, "catalog_filtered_by_drive.json")
    with open(filtered_drive_path, "w", encoding="utf-8") as file:
        json.dump(filtered_by_drive, file, ensure_ascii=False, indent=4)
    print(f"Данные каталога, отфильтрованные по приводу, сохранены в файл: {filtered_drive_path}")

    # 3. Статистика по мощности, л.с.
    power_values = [int(item['Параметры'].get('Мощность, л.с.', 0)) for item in catalog_data]
    if power_values:
        avg_power = sum(power_values) / len(power_values)
        max_power = max(power_values)
        min_power = min(power_values)
        power_stats = {
            "average_power": avg_power,
            "max_power": max_power,
            "min_power": min_power
        }
        power_stats_path = os.path.join(output_folder, "catalog_power_stats.json")
        with open(power_stats_path, "w", encoding="utf-8") as file:
            json.dump(power_stats, file, ensure_ascii=False, indent=4)
        print(f"Статистика по мощности сохранена в файл: {power_stats_path}")

    # 4. Частота типов автомобилей
    car_types = [item['Тип авто'] for item in catalog_data]
    type_counts = {}
    for car_type in car_types:
        type_counts[car_type] = type_counts.get(car_type, 0) + 1
    type_counts_path = os.path.join(output_folder, "catalog_car_type_counts.json")
    with open(type_counts_path, "w", encoding="utf-8") as file:
        json.dump(type_counts, file, ensure_ascii=False, indent=4)
    print(f"Частота типов автомобилей сохранена в файл: {type_counts_path}")


# Запуск основной функции
catalog_url = "https://ekb.arendacar.ru/"
scrape_and_save_all(catalog_url)
