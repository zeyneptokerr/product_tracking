import requests

from bs4 import BeautifulSoup
from ..database import db_operations


class SearchHepsiBurada():
    def search_hepsiburada(product_id, product_name):
        if " " in product_name:
            product_name = product_name.replace(" ", "+")

        url = f"https://www.hepsiburada.com/ara?q={product_name}"
        headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" }
        page = requests.get(url, headers=headers)
        soup=BeautifulSoup(page.content, 'html.parser')

        products = soup.find_all("li", {"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})
        for product in products:
            # ürünün başlığını alıyoruz
            try:
                product_title = product.find_all("h3", {"data-test-id": "product-card-name"})
                product_title = product_title[0].text
            except Exception as e:
                print("Product Title Error:", e)
            
            # ürünün fiyatını alıyoruz
            try:
                product_price = product.find_all("div", {"data-test-id":"price-current-price"})
                product_price = int(product_price[0].text.split(",")[0].replace(".",""))
            except Exception as e:
                print("Product Price Error:", e)

            # ürünün linkini alıyoruz
            try:
                product_link = product.a.get('href')
                product_link = "https://www.hepsiburada.com" + product_link
            except Exception as e:
                print("Product Link Error:", e)

            # ürün bilgilerini db'ye basıyoruz
            db_operations.product_tracking(product_id, product_link, product_price)


    def get_hepsiburada_for_dyson_detail():
        url = "https://www.hepsiburada.com/dyson-v12-detect-slim-absolute-kablosuz-supurge-pm-HBC00002CO32L"
        headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" }
        page = requests.get(url, headers=headers)
        soup=BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all("div", {"class": "product-price price-container big"})
        price = int(div[0].find_all('del', attrs={"class": "price-old"})[0].text.split(",")[0].replace(".",""))
        print(price)