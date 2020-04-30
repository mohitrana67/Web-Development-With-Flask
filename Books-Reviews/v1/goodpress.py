import requests

class GetRatings:

    def __init__(self,book_isbn):
        self.isbn = book_isbn
    
    def ratings(self):
        self.res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "YBryP3SOsomoImeJpFYAbg", "isbns":self.isbn})
        self.data = self.res.json()

        self.book_total_review = self.data['books'][0]['work_ratings_count']
        self.book_average_rating = self.data['books'][0]['average_rating']

        return (self.book_total_review, self.book_average_rating)