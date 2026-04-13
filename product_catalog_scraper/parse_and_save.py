import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from db import engine, session
from models import Base, Book


BASE_URL = "https://books.toscrape.com/"


COLUMNS = {'title':('h1', {}), 'price':('p', {'class':'price_color'}), 
            'category':('a', {'href': re.compile(r'^\.\./category/books/[^/]+/index\.html$')}), 
            'rating':('p', {'class': re.compile(r'^star-rating')}),
}

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5} 


def parse_books_url(url):
    """Парсинг ссылок на страницы книг"""
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find('li', class_="current").get_text()
    matches = re.findall(r'\d+', text)
    num_of_pages = int(matches[-1])
    book_urls = set() 
    for pg in range(1, num_of_pages+1):
        response = requests.get(url + f'catalogue/page-{pg}.html')
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            if (href.endswith('index.html') and 
                '_' in href and 
                'category/books' not in href):

                full_url = url + 'catalogue/' + href
                book_urls.add(full_url)

    return list(book_urls)


def parse_book_info(url):
    """Парсинг информации о книге"""
    http_session = requests.Session()
    response = http_session.get(url) 
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    dict_info = {}
    for col, (tag, attrs) in COLUMNS.items():
        element = soup.find(tag, attrs=attrs)
        if col == 'rating':
            rating = element.get('class')[1]
            dict_info[col] =  RATING_MAP[rating]
            dict_info['book_url'] = url

        else:
            value = element.get_text()
            dict_info[col] = value if col != 'price' else float(value[1:])

    return dict_info


def save_books_to_db(BASE_URL):
    book_urls = parse_books_url(BASE_URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session = session()

    def process_and_add(url):
        try:
            info = parse_book_info(url)
            book = Book(
                title=info['title'],
                price=info['price'],
                category=info['category'],
                rating=info['rating'],
                book_url=info['book_url'],
                parsed_at=datetime.utcnow()
            )
            return book
        except Exception as e:
            print(f"Ошибка при парсинге {url}: {e}")
            return None

    print(f"Сохранение {len(book_urls)} книг")
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(process_and_add, book_urls))

    books_to_save = [b for b in results if b is not None]
    db_session.add_all(books_to_save)
    db_session.commit()
    
    print(f"Успешно сохранено {len(books_to_save)} книг.")
    db_session.close()

    
# save_books_to_db(BASE_URL)
