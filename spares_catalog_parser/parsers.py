import re



def detect_type(soup):
    if soup.find("div", class_="price"):
        return "product"
    if soup.find("td", class_="td_price"):
        return "предоставляемые услуги"
    return "unknown"


def clean_price(text):
    return re.sub(r'\D', '', text) if text else None


def parse_product_prices(soup):
    price = soup.find("div", class_="price")
    price_without = soup.find("div", class_="price_without")

    return {
        "цена с учетом обмена": clean_price(price.text.strip()) if price else None,
        "цена без обмена": clean_price(price_without.text.strip()) if price_without else None
    }


def get_value_by_param(soup, param_name):
    if not soup:
        return None

    param_span = soup.find('span', class_='param', string=lambda t: t and param_name in t)
    if param_span:
        value_span = param_span.find_next_sibling('span', class_='value')
        return value_span.get_text(strip=True) if value_span else None
    return None


def parse_services(soup):
    rows = soup.find_all("tr")
    services = []

    for row in rows:
        name = row.find("td", class_="td_name")
        price = row.find("td", class_="td_price")

        if name and price:
            services.append({
                "name": name.text.strip(),
                "price": clean_price(price.text.strip())
            })

    return services if services else None


def get_all_numbers(soup):
    table = soup.find('table', id='catalog_numbers_orig')
    if not table:
        return None

    numbers = []
    rows = table.find('tbody').find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            numbers.append({
                'orig': cols[0].get_text(strip=True),
                'extra': cols[1].get_text(strip=True)
            })

    return numbers


def get_usability(soup):
    table = soup.find('table', id='usability')
    if not table:
        return None

    usability_list = []
    rows = table.find('tbody').find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 6:
            usability_list.append({
                'brand': cols[0].get_text(strip=True),
                'model': cols[1].get_text(strip=True),
                'modification': cols[2].get_text(strip=True),
                'engine': cols[3].get_text(strip=True),
                'drive': cols[4].get_text(strip=True),
                'years': cols[5].get_text(strip=True)
            })

    return usability_list