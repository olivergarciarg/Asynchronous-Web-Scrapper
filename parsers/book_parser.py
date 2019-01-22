import re
import logging

from locators.book_locators import BookLocators

logger = logging.getLogger('scraping.book_parser')

class BookParser:
    """
    A class tot ake in an HTML page (or part of it), and find properties of an item in it
    """

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        #logger.debug(f'New book parser created from `{parent}`.')
        logger.debug(f'New book parser created from `TBD`.')
        self.parent = parent      # parent is already BeautifulSoup object

    def __repr__(self):
        return f'<Book {self.name}, £{self.price} ({self.rating} stars)>'

    # optional "@property", because is a read only method
    @property
    def name(self):
        logger.debug('Finding book name...')
        locator = BookLocators.NAME_LOCATOR    # or 'article h3 a' ---CSS locator
        item_link = self.parent.select_one(locator)
        item_name = item_link.attrs['title']
        logger.debug(f'Found book name, `{item_name}`.')
        return item_name

    @property
    def link(self):
        logger.debug('Finding book link...')
        locator = BookLocators.LINK_LOCATOR    # or 'article h3 a' ---CSS locator
        item_link = self.parent.select_one(locator).attrs['href']
        logger.debug(f'Found book link, `{item_link}`.')
        return item_link

    @property
    def price(self):
        logger.debug('Finding book price...')
        locator = BookLocators.PRICE_LOCATOR
        item_price = self.parent.select_one(locator).string
        pattern = '£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        float_price = float(matcher.group(1))
        logger.debug(f'Found book price, `{float_price}`.')
        return float_price

    @property
    def rating(self):
        logger.debug('Finding book rating...')
        locator = BookLocators.RATING_LOCATOR
        star_rating_tag = self.parent.select_one(locator)
        classes = star_rating_tag.attrs['class']    # ['star-rating', 'Three']
        rating_classes = [rating for rating in classes if rating != 'star-rating']
            # or rating_classes = filter(lambda x: x != 'star-rating', classes)
        rating_number = BookParser.RATINGS.get(rating_classes[0])       # None if not found
        # or return 0 if not found
        # rating_number = BookParser.RATINGS.get(rating_classes[0],0)
        logger.debug(f'Found book rating, `{rating_number}`.')
        return rating_number