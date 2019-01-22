import re
import logging
from bs4 import BeautifulSoup

from locators.all_books_page import AllBooksPageLocators
from parsers.book_parser import BookParser

logger = logging.getLogger('scraping.all_books_page')

class AllBooksPage:
    def __init__(self, page_content):
        logger.debug('Parsing page content with BeautifulSoup HTML parser.')
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Finding all books in the page using `{AllBooksPageLocators.BOOKS}`.')
        return [BookParser(e) for e in self.soup.select(AllBooksPageLocators.BOOKS)]    # returns several book parser object

    @property
    def page_count(self):
        logger.debug(f'Finding all number of catalogue pages available using `{AllBooksPageLocators.PAGER}`.')
        content = self.soup.select_one(AllBooksPageLocators.PAGER).string
        logger.debug(f'Found number of catalogue pages available: `{content}`.')
        #print(content)
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        #print(pages)
        logger.debug(f'Extracted number of pages as integer: `{pages}`.')
        return pages
