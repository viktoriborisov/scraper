import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

START_URL = f'https://webscraper.io/test-sites/e-commerce/scroll'

product_ids = []
product_urls = []
product_titles = []
product_descrs = []
product_prices = []


def get_data_from_url(driver: WebDriver):
    div_items = driver.find_elements(By.CLASS_NAME, 'ecomerce-items')
    if len(div_items) != 0:
        for dict_data in json.loads(div_items[0].get_attribute("data-items")):
            product_ids.append(dict_data["id"])
            product_urls.append(f'https://webscraper.io/test-sites/e-commerce/scroll/product/{dict_data["id"]}')
            product_titles.append(dict_data["title"])
            product_descrs.append(dict_data["description"])
            product_prices.append(dict_data["price"])


def find_all_links(url: str, all_finded_urls: set):
    driver = webdriver.Chrome()
    driver.get(url)
    div_navbar = driver.find_elements(By.CLASS_NAME, "navbar-default")
    a_elements = div_navbar[0].find_elements(By.TAG_NAME, "a")
    finded_urls = [elem.get_attribute('href') for elem in a_elements]

    for _ in finded_urls:
        full_path = f'{_}'
        if full_path not in all_finded_urls and full_path != START_URL:
            all_finded_urls.add(full_path)
            get_data_from_url(driver)
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
