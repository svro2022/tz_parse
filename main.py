import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Установка прокси-сервера
# выбранный рабочий прокси в формате "http://IP:Порт"
proxy = "http://176.115.79.195:1080"
proxies = {
    "http": proxy,
    "https": proxy,
}


# Функция получения данных о товарах на странице категории
def parse_category_page(category_url):
    response = requests.get(category_url, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Получение списка товаров в категории
    products = soup.find_all('div', class_='product-item')

    data = []

    for product in products:
        # Категория товара
        category = product.find(class_='product-page').text.strip()
        # Наименование товара
        product_name = product.find(class_='product-page__title').text.strip()
        # Ссылка на изображение товара
        image_url = product.find('img', class_='product-left__slider')['src']
        # Цена
        price = product.find(class_='product-card__price-tag__price').text.strip()
        # Описание
        description = product.find('p', class_='product-right__description card-txt').text.strip()

        item_data = {
            "Категория товара": category,
            "Наименование товара": product_name,
            "Ссылка на изображение товара": image_url,
            "Цена": price,
            "Описание": description
        }

        data.append(item_data)

    return data


# Установка настроек для браузера
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск браузера без графического интерфейса
chrome_options.add_argument("--no-sandbox")  # Опция для Linux
chrome_options.add_argument("--disable-dev-shm-usage")  # Опция для Linux

# Установка прокси-сервера для браузера
capabilities = webdriver.DesiredCapabilities.CHROME.copy()
capabilities['proxy'] = {
    'httpProxy': proxy,
    'ftpProxy': proxy,
    'sslProxy': proxy,
    'proxyType': 'MANUAL',
}

# Инициализация драйвера Chrome
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options, desired_capabilities=capabilities)

# Список страниц категорий для парсинга
category_urls = [
    "https://bristol.ru/category/135",  # Фрукты, овощи
    "https://bristol.ru/category/139"  # Снэки
]

# Итерация по страницам категорий и парсинг данных
all_data = []
for category_url in category_urls:
    category_data = parse_category_page(category_url)
    all_data += category_data

# Сохранение данных в файл JSON
with open('data.json', 'w') as file:
    json.dump(all_data, file, indent=4, ensure_ascii=False)

# Закрытие браузера и освобождение ресурсов
driver.quit()

print("Парсинг завершен и данные сохранены в файл 'data.json'")
