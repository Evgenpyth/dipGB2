import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Функция для парсинга страницы и извлечения информации о продуктах
def parse_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', class_='dtList i-dtList j-card-item')

        # Списки для хранения данных о продуктах
        product_names = []
        prices = []
        descriptions = []
        brands = []
        urls = []

        # Извлечение информации о каждом продукте на странице
        for product in products:
            product_name = product.find('span', class_='goods-name').text.strip()
            price = product.find('span', class_='price').text.strip()
            description = product.find('div', class_='goods-description').text.strip()
            brand = product.find('strong', class_='brand-name').text.strip()
            url = product.find('a', class_='ref_goods_n_p')['href']

            # Добавление данных о продукте в соответствующие списки
            product_names.append(product_name)
            prices.append(price)
            descriptions.append(description)
            brands.append(brand)
            urls.append(url)

        # Создание DataFrame из собранных данных
        df = pd.DataFrame({
            'Product Name': product_names,
            'Price': prices,
            'Description': descriptions,
            'Brand': brands,
            'URL': urls
        })

        return df
    else:
        print('Ошибка при выполнении запроса:', response.status_code)
        return None

# Главная функция для выполнения парсинга
def main():
    base_url = 'https://catalog-ads.wildberries.ru/api/v6/catalog?menuid=9492'
    pages = range(1, 6)  # Парсинг первых 5 страниц

    # Список для хранения DataFrame каждой страницы
    dfs = []

    # Парсинг каждой страницы и добавление DataFrame в список
    for page in pages:
        url = f'{base_url}?page={page}'
        df = parse_page(url)
        if df is not None:
            dfs.append(df)
            time.sleep(5)  # Задержка между запросами для увеличения интервала

    # Объединение всех DataFrame в один и сохранение в файл Excel
    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        result_df.to_excel('wildberries_products.xlsx', index=False)
        print('Данные успешно записаны в файл wildberries_products.xlsx')
    else:
        print('Не удалось собрать данные.')

if __name__ == '__main__':
    main()