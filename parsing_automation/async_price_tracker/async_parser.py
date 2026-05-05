import asyncio
from bs4 import BeautifulSoup
from sqlalchemy import text
from db import engine, session
from models import PremiumBook
from config import HEADERS, URL



semaphore = asyncio.Semaphore(10)


def clear_database():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE premium_books;"))


async def fetch_page(session, url):
    async with semaphore:
        try:
            async with session.get(url, headers=HEADERS, timeout=30) as response:
                return await response.text()
        except Exception as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None
        
    
async def parse_single_page(http_session, page_num):
    os_param = (page_num - 1) * 20
    url = f"{URL}?os={os_param}" if os_param > 0 else URL
    
    html = await fetch_page(http_session, url)
    if not html:
        return 0

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='twr')
    count = 0
    if items:
        with session() as db_session:
            
            for item in items:
                base_url = 'https://podarochnieknigi.ru'
                book_url = base_url + item.find('h2', class_='twr-name').a['href']
                name = item.find('h2', class_='twr-name').text.strip()
                price_str = item.find('div', class_='twr-inner-price').text.strip().replace(' ', '').replace('руб', '')
                price = float(price_str)
                image_link = base_url + item.find('img', class_='twr-img-prew')['src'].replace('_250x250', '')

                book = PremiumBook(title=name, price=price, book_url=book_url, image_link=image_link)
                db_session.add(book)

                count += 1
            db_session.commit()
    return count