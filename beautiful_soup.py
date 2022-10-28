import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

SITE_URI = "https://webscraper.io"
START_URL = f'{SITE_URI}/test-sites/e-commerce/scroll'

product_ids = []
product_urls = []
product_titles = []
product_descrs = []
product_prices = []


def get_data_from_url(soup: BeautifulSoup):
    div_item = soup.find('div', class_='ecomerce-items')
    if div_item is not None:
        for dict_data in json.loads(div_item['data-items']):
            product_ids.append(dict_data["id"])
            product_urls.append(f'https://webscraper.io/test-sites/e-commerce/scroll/product/{dict_data["id"]}')
            product_titles.append(dict_data["title"])
            product_descrs.append(dict_data["description"])
            product_prices.append(dict_data["price"])


def find_all_links(url: str, all_finded_urls: set):
    response = requests.get(url)
    if not 200 <= response.status_code < 300:
        print(f'URL {url} недоступен. Код ответа - {response.status_code}')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        finded_urls = soup.find('div', role='navigation').find_all('a')
        for _ in finded_urls:
            full_path = f'{SITE_URI}{_["href"]}'
            if full_path not in all_finded_urls and full_path != START_URL:
                all_finded_urls.add(full_path)
                get_data_from_url(soup)
                find_all_links(url=full_path, all_finded_urls=all_finded_urls)

all_urls = set()
find_all_links(url=START_URL,
               all_finded_urls=all_urls)

df = pd.DataFrame({'Product ID': product_ids,
                   'URL': product_urls,
                   'Title': product_titles,
                   'Description': product_descrs,
                   'Price': product_prices})

with open('out_stat.csv', 'w', encoding='utf8') as file:
    file.write(df.to_csv(index=False, lineterminator='\n'))
