import aiohttp
import asyncio
from async_parser import *

async def main():
    clear_database()

    async with aiohttp.ClientSession() as session:
        first_page = await fetch_page(session, URL)
        
        soup = BeautifulSoup(first_page, 'html.parser')
        pages_block = soup.find('div', id='pages')
        num_of_pages = int(pages_block.find_all('a')[-1].text) if pages_block else 1
        tasks = [parse_single_page(session, p) for p in range(1, num_of_pages + 1)]
        results = await asyncio.gather(*tasks)
        
        print(f"\Всего собрано товаров: {sum(results)}")


if __name__ == "__main__":
    asyncio.run(main())