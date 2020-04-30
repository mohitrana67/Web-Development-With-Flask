import csv
import os

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

# engine = create_engine("postgres://pvvjoazaealpqs:4d4ce3e1d242705bfd1904bf5edff3e88437f8135c9b0be9b07e2f9df4468948@ec2-54-83-202-132.compute-1.amazonaws.com:5432/d9i9akof301l1j")
# db = scoped_session(sessionmaker(bind=engine))

def addBooks():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if title == 'Aztec':
            print (f"Book name is {title}")
    #     db.execute("INSERT INTO books (book_isbn, book_title, book_author, book_year_published) VALUES (:book_isbn, :book_title, :book_author, :book_year_published)",
    #                {"book_isbn": isbn, "book_title": title, "book_author": author, "book_year_published": year})
    #     print(f"{title} is written by {author} in {year} under {isbn}")
    # db.commit()

def main():
    addBooks()

if __name__ == "__main__":
    main()
