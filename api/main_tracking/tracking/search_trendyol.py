import json
import requests

from bs4 import BeautifulSoup
from ..database import db_operations


class SearchTrendyol:
    def search_trendyol(product_id, product_name):
        if " " in product_name:
            product_name = product_name.replace(" ","%20")

        url = f"""https://public-mdc.trendyol.com/discovery-search-websfxsuggestions-santral/api/suggestions?culture=tr-TR&text={product_name}&searchTestParameter=Suggestion_A%2CSuggestionBadges_A%2CSuggestionStoreAds_B&platform=WEB"""

        response = requests.get(url).text
        response_json = json.loads(response)
        target_url = response_json["result"][0]["targetUrl"]
        target_url = "https://www.trendyol.com" + target_url.replace("\u0026", "&")

        page = requests.get(target_url)
        soup=BeautifulSoup(page.content, 'html.parser')
        div_list = soup.find_all("div", {"class": "prdct-cntnr-wrppr"})
        for div in div_list:
            products = div.find_all("div", {"class": "p-card-chldrn-cntnr card-border"})
            for index, product in enumerate(products):
                # ürünün linkini alıyoruz
                try:
                    product_link = product.a.get('href')
                    product_link = "https://www.trendyol.com" + product_link
                except Exception as e:
                    print("Product Link Error:", e)

                # ürünün markasını alıyoruz
                try:
                    product_brand = product.find_all("span", {"class": "prdct-desc-cntnr-ttl"})[0].text
                except Exception as e:
                    print("Product Brand Error:", e)

                # ürünün başlığını alıyoruz
                try:
                    product_title = product.find_all("span", {"class": "prdct-desc-cntnr-name"})[0].text
                except Exception as e:
                    print("Product Title Error:", e)

                # ürünün fiyatını alıyoruz
                try:
                    product_price = div.find_all("div", {"class": "prc-box-dscntd"})[index]
                    product_price = product_price.text.split(" ")[0].split(",")[0].replace(".","")
                except Exception as e:
                    print("Product Price Error:", e)

                # db'ye product link ekle, yorum sayısını ekle, yıldız sayısını ekle, ürünün markasını ayrı bi kolon olarak ekle

                # ürün bilgilerini db'ye basıyoruz
                db_operations.product_tracking(product_id, product_link, product_price)


    def get_trendyol_for_dyson_detail():
        url = "https://www.trendyol.com/dyson/v12-detect-slim-extra-absolute-kablosuz-supurge-p-376110043?boutiqueId=61&merchantId=243893"
        page = requests.get(url)
        soup=BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all("div", {"class": "pr-bx-nm with-org-prc"})
        price = int(div[0].span.text.split(" ")[0].replace(".",""))
        print(price)