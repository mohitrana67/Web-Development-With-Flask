class Books:

    counter = 1

    def __init__(self,title,author,isbin,date):
        #setting id of the book to be a counter
        self.id = Books.counter

        #incrementing the counter every time a book is being creaeted
        Books.counter += 1
        
        #keepinf track of every author who bought this book.
        self.buyer = []

        #all the information about the book
        self.title_of_book = title
        self.author_of_book = author
        self.isbn_for_book = isbin
        self.date_published = date
    
    def prinfInfo(self):
        print(f"Title of book is {self.title_of_book}")
        print(f"Autho of {self.title_of_book} is {self.author_of_book}")
        print(f"{self.author_of_book} wrote {self.title_of_book} on {self.date_published} under the ISBN {self.isbn_for_book}")
        print(f"list of authors for this books is {self.buyer}")

    #add authors to the list of books
    def addAuthor(self,name_of_buyer):
        self.buyer.append(name_of_buyer)

class Authors:
    def __init__(self,name):
        self.name_of_buyer = name
        
def main():
    book1 = Books(title="This is new",author="Mohit Rana",isbin=12345,date="11-02-2019")

    print(book1.title_of_book)

    book1.title_of_book = "This is the updated name"

    author1 = Authors("M")
    author2 = Authors("R")
    book1.addAuthor(author1)
    book1.addAuthor(author2)
    book1.prinfInfo()

if __name__ == "__main__":
    main()