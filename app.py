import requests
import aiohttp
import async_timeout
import asyncio
import time
import logging

from pages.all_books_page import AllBooksPage

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename='logs.txt')

logger = logging.getLogger('scraping')

logger.info('Loading books list...')

page_content = requests.get('http://books.toscrape.com').content

page = AllBooksPage(page_content)       # builds page object

loop = asyncio.get_event_loop()

books = page.books      #returns the books using the method books from pages.all_books_page


async def fetch_page(session, url):
    page_start = time.time()
    # async with aiohttp.ClientSession() as session:
    async with async_timeout.timeout(10):               # to terminate a session if it takes too long
        async with session.get(url) as response:
            print(f'page loaded in {time.time() - page_start}')
            #return response.status
            return await response.text()      #response.text() is the HTML content of the page


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:     #(loop=loop) pass loop as the previously created loop so this line doesn't create a new loop
        for url in urls:
            #tasks.append(fetch_page(url))
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)      # gathering all the tasks in our listing an treating them as a single list sp we can execute them in a list
        return await grouped_tasks          # this function will RETURN something when grouped_tasks finishes


urls = [f'http://books.toscrape.com/catalogue/page-{page_num + 1}.html' for page_num in range(1, page.page_count)]
start = time.time()
pages = loop.run_until_complete(get_multiple_pages(loop, *urls))
print(f'Total page requests took {time.time()- start}')

for page_content in pages:
    logger.debug('Creating AllBooksPage from page_content.')
    page = AllBooksPage(page_content)
    books.extend(page.books)

"""
#logger.debug(f'Found `{page.page_count}` pages.')
for page_num in range(1, page.page_count):
    url = f'http://books.toscrape.com/catalogue/page-{page_num + 1}.html'
    logger.debug(f'Trying to connect to `{url}`.')
    page_content = requests.get(url).content
    logger.debug('Creating AllBooksPage from page_content.')
    page = AllBooksPage(page_content)
    books.extend(page.books)
"""