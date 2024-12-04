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


# Основная функция
catalog_url = "https://ekb.arendacar.ru/"  # Укажите правильный URL каталога

# Создаем папку для сохранения данных
output_folder = "задание5"
os.makedirs(output_folder, exist_ok=True)


# Функция для извлечения данных и сохранения в файл
def scrape_and_save(catalog_url):
    print("Скачивание страницы каталога...")
    html_content = download_page(catalog_url)

    if html_content:
        # Парсим страницу с помощью BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Ищем все элементы с классом 'main-top-cars__item'
        main_top_cars_items = soup.find_all("div", class_="main-top-cars__item")

        # Если элементы найдены, извлекаем нужную информацию
        if main_top_cars_items:
            products = []
            for item in main_top_cars_items:
                # Извлекаем информацию из блока cars-item-2__info
                info_block = item.find("div", class_="cars-item-2__info")
                if info_block:
                    # Извлекаем название автомобиля
                    name = info_block.find("span", class_="cars-item-2__heading").text.strip()
                    # Извлекаем тип автомобиля
                    status = info_block.find("div", class_="cars-item-2__status").text.strip()

                    # Извлекаем параметры автомобиля
                    params = {}
                    param_elements = info_block.find_all("div", class_="cars-item-2__param")
                    for param in param_elements:
                        label = param.find("div", class_="cars-item-2__param_label").text.strip()
                        value = param.find("div", class_="cars-item-2__param_value").text.strip()
                        params[label] = value

                    # Извлекаем цену из блока cars-item-2-control__price
                    price_block = item.find("div", class_="cars-item-2-control__price")
                    if price_block:
                        # Извлекаем цену из атрибута data-price
                        price_data = price_block.get("data-price")
                        if price_data:
                            price_list = json.loads(price_data)
                            for price_info in price_list:
                                if price_info.get("days_min") == 30 and price_info.get("days_max") == 999:
                                    price_value = price_info.get("price", "Цена не найдена")

                                    # Добавляем данные в список
                                    products.append({
                                        "Название": name,
                                        "Тип авто": status,
                                        "Параметры": params,
                                        "Цена (в рублях)": price_value,
                                        "Единица измерения": "руб."
                                    })

            # Сохраняем данные в файл
            output_path = os.path.join(output_folder, "products.json")
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(products, file, ensure_ascii=False, indent=4)
            print(f"Данные о товарах сохранены в {output_path}.")
        else:
            print("Не удалось найти элементы с классом 'main-top-cars__item'.")
    else:
        print("Не удалось скачать страницу.")


# Вызов функции для скачивания и сохранения данных
scrape_and_save(catalog_url)
