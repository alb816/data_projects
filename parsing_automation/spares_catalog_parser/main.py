from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from parsers import detect_type, get_all_numbers, get_value_by_param, get_usability, parse_product_prices, parse_services



def parse_page(url, parsed):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        ul_items = soup.find("ul", class_="items")

        page_type = detect_type(soup)

        result = {
            "каталожный номер": parsed.get("catalog_num"),
            "наименование": parsed.get("name"),
            "оригинальные и дополнительные номера": json.dumps(get_all_numbers(soup), ensure_ascii=False),
            "производитель АКПП": get_value_by_param(ul_items, "Производитель АКПП"),
            "марка АКПП": get_value_by_param(ul_items, "Марка АКПП"),
            "применяемость к автомобилям": json.dumps(get_usability(soup), ensure_ascii=False),
            "предоставляемые услуги": None,
            "цена с учетом обмена": None,
            "цена без обмена": None
        }
        if page_type == "product":
            result.update(parse_product_prices(soup))

        elif page_type == "предоставляемые услуги":
            services = parse_services(soup)
            result["предоставляемые услуги"] = json.dumps(services, ensure_ascii=False) if services else None
        return result

    except Exception:
        return None
    

def main():
    url = "https://transfix.su/catalog/ajax?page=1"
    page_count = 0
    results = []

    while url and page_count < 2:
        res = requests.get(url)
        try:
            data = res.json()
        except requests.exceptions.JSONDecodeError:
            print("Ответ был не в формате JSON.", res.text)

        items = data["items"]["data"]

        for item in items:
            soup = BeautifulSoup(item["html"], "html.parser")
            link = soup.find("a")["href"]

            parsed = {
                "catalog_num": item["article"],
                "name": item["name"]
            }

            result = parse_page(link, parsed)

            if result:
                results.append(result)


        url = data.get("more")
        page_count += 1

    df = pd.DataFrame(results)
    df.to_excel("transfix_catalog.xlsx", index=False)


if __name__ == "__main__":
    main()