from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import sys
import json

url = 'https://shopee.co.id/search?keyword=bahan%20kain&page=0'

# options = Options()
browser = webdriver.Chrome(
    "chromedriver.exe")


def search(base_url):
    browser.get(base_url)
    time.sleep(5)
    browser.execute_script('window.scrollTo(0, 1500);')
    time.sleep(5)
    browser.execute_script('window.scrollTo(0, 2500);')
    time.sleep(5)
    html = browser.page_source
    # browser.close()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('li', {"class": "b-catalogList__itm"})
    data = []
    for x, div in enumerate(table):
        tag_link = div.find("a")
        if tag_link is not None:
            data.append(tag_link.get('href'))

    return data


all_data = []
counter = 0
while (counter <= 5):
    if counter > 4:
        counter = 1
    counter += 1
    base_url = 'https://www.zalora.co.id/catalog/?page=' + \
        str(counter)+'&q=Celana+Jeans+Stretch+Pria'
    product_urls = search(base_url)

    for index, product_url in enumerate(product_urls):
        url_detail = 'https://www.zalora.co.id/' + product_url
        browser.get(url_detail)
        time.sleep(5)
        browser.execute_script('window.scrollTo(0, 1500);')
        time.sleep(5)
        browser.execute_script('window.scrollTo(0, 2500);')
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        merek = soup.find("div", class_='js-prd-brand').text
        fix_merek = "".join(merek.split())

        product_name = soup.find('div', class_='product__title').text

        price = soup.find(
            "span", {"id": "js-detail_price_without_selectedSize"}).text
        fix_price = "".join(price.split())

        data_produk = dict()
        data_produk["marketplace_name"] = 'zalora'
        data_produk["link"] = url_detail
        data_produk["merek"] = fix_merek
        data_produk["nama_produk"] = product_name
        data_produk["harga"] = fix_price

        with open("data_zalora.json", "a") as data:
            data.write(json.dumps(data_produk) + ', ')
            data.close()

        sys.exit()
# if all_data:
        # x = collection.insert_many(all_data)
