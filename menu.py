import logging
from app import books

logger = logging.getLogger('scraping.menu')


USER_CHOICE = """
Enter one of the following
- 'b' to look at 5 star books
- 'c' to look at the cheapest books
- 'n' to just get the next available book on the page
- 'q' to exit

Enter your choice: 
"""

def print_best_books():
    logger.info('Finding best books by rating...')
    best_books = sorted(books, key = lambda x: x.rating * -1)[:10]        # best_books contains the books sorted by rating, the last part [:10] limits the list to 10 books
    for book in best_books:
        print(book)

# to sort by 2 variables
def print_best_cheap_books():
    logger.info('Finding best books cheap books by price...')
    best_books = sorted(books, key = lambda x: (x.rating * -1, x.price))[:10]        # best_books contains the books sorted by rating, the last part [:10] limits the list to 10 books
    for book in best_books:
        print(book)


def print_cheapest_books():
    logger.info('Finding cheapest books by price...')
    cheapest_books = sorted(books, key = lambda x: x.price)[:10]        # best_books contains the books sorted by rating, the last part [:10] limits the list to 10 books
    for book in cheapest_books:
        print(book)


books_generator = (x for x in books)

def get_next_book():
    print(next(books_generator))

#print_best_books()
#print_cheapest_books()
#print_best_cheap_books()


# another option for menu
user_choices = {
    'b': print_best_books,
    'c': print_cheapest_books,
    'n': get_next_book
}


def menu():
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input in ('b', 'c', 'n'):
            user_choices[user_input]()      # calls the function associated in the user_choices dictionary
        else:
            print('Please choose a valid command.')
        user_input = input(USER_CHOICE)
    logger.debug('Terminating program...')


"""
def menu():
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == 'b':
            print_best_books()
        elif user_input == 'c':
            print_cheapest_books()
        elif user_input == 'n':
            get_next_book()
        else:
            print('Please choose a valid command.')
        user_input = input(USER_CHOICE)
"""

menu()