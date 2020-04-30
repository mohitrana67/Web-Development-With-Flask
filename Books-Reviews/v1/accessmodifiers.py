class Books:

    def __init__(self, book_title, book_author, book_isbn, book_year):
        self.book_title = book_title
        self.book_author = book_author
        self.book_isbn = book_isbn
        self.book_year = book_year
    
    def add_book(self,book):
        print(self.book_author)
