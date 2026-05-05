import requests
from bs4 import BeautifulSoup
from config import URL


def parse_data():
    data = []

    for page in range(1, 10):
        url = f"{URL}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("li", class_="product")
        for item in items:
            name = item.find("h2", class_="woocommerce-loop-product__title").text
            price = item.find("span", class_="woocommerce-Price-amount").text
            price = price.replace("£", "")
            price = float(price)
            link = item.find("a")["href"]
            data.append({"name": name, "price in £": price, "url": link})
    return data