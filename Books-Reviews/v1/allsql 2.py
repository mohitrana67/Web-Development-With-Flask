import os
import hashlib, binascii, os

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from goodpress import *
# Set up database
engine = create_engine("postgres://pvvjoazaealpqs:4d4ce3e1d242705bfd1904bf5edff3e88437f8135c9b0be9b07e2f9df4468948@ec2-54-83-202-132.compute-1.amazonaws.com:5432/d9i9akof301l1j")
db = scoped_session(sessionmaker(bind=engine))

class Book:
    def __init__(self,book_id,user):
        self.book_id = book_id
        self.user = user

    def select(self):
        book = db.execute("SELECT * from books WHERE id = :book_id",{"book_id":self.book_id}).fetchone()
        self.book_isbn = book[1]
        self.book_title = book[2]
        self.book_author = book[3]
        self.book_year = book[4]
        return (self.book_title,self.book_author,self.book_isbn,self.book_year)
    
    def add_review(self,review,rating):
        self.review = review
        self.rating = int(rating)
        self.user_credentials = Users()
        self.result = self.user_credentials.select(self.user,1)
        db.execute("INSERT into book_reviews(user_id,book_id,book_review,book_rating) VALUES(:user_id,:book_id,:book_review,:book_rating)",{"user_id":self.result[0],"book_id":self.book_id,"book_review":self.review,"book_rating":self.rating})
        db.commit()
    
    def check_previous_review(self):
        self.user_data =Users()
        self.user_id = self.user_data.select(self.user,1)[0]
        self.user_review_rowcount = db.execute("SELECT * from book_reviews where user_id = :user_id and book_id = :book_id",{"user_id":self.user_id,"book_id":self.book_id}).fetchall()
        if len(self.user_review_rowcount) == 0:
            return False
        else:
            return True

class Users:

    def select(self,user,flag):
        self.user = user
        self.flag = flag
        self.user_data = db.execute("SELECT * from user_credentials where user_username = :user",{"user":self.user}).fetchone()
        if self.flag == 1:
            self.user_id = self.user_data[0]
            self.user_username = self.user_data[1]
            self.user_password = self.user_data[2]
            return (self.user_id,self.user_username,self.user_password)
        elif self.flag == 0:
            if self.user_data == None :
                return False
            else:
                return True
            # return (self.user_data == None)
    
    def insert_user_credentials(self,username,hashed_password,fname, lname, phone_number,country, province, city, postal_code):
        #for adding data in user_credentials table
        db.execute("INSERT into user_credentials(user_username, user_password) VALUES(:user_username, :user_password)",{"user_username":username, "user_password":hashed_password})
        db.commit()
        
        #creating an instance of the class Users
        self.user_data = Users()

        #calling select method to get the user_id
        self.user_id = self.user_data.select(username,1)[0]
        
        # creating local variable for the scope of this assignment
        self.fname = fname
        self.lname = lname
        self.phone_number = phone_number
        self.country = country
        self.province = province
        self.city = city
        self.postal_code = postal_code
        # calling insert method to insert user data into database
        self.user_data.insert_user_data(self.user_id,self.fname, self.lname, self.phone_number, self.country, self.province, self.city, self.postal_code)

    def insert_user_data(self,user_id,fname,lname, phone_number, country, province, city, postal_code):
        self.user_id = user_id
        self.fname = fname
        self.lname = lname
        self.phone_number = phone_number
        self.country = country
        self.province = province
        self.city = city
        self.postal_code = postal_code
        #for adding data in the user_data table
        db.execute("INSERT into user_data(user_id,user_first_name,user_last_name,user_phone_number,user_country,user_province,user_city,user_postal_code) VALUES(:user_id,:fname,:lname,:phone_number,:country,:province,:city,:postal_code)", {"user_id":user_id,"fname":fname,"lname":lname,"phone_number":phone_number,"country":country,"province":province,"city":city,"postal_code":postal_code})
        db.commit()

class API():

    def search_by_isbn(self,isbn):
        self.isbn = str(isbn)
        self.book = db.execute("SELECT * from books where book_isbn =:isbn",{"isbn":self.isbn}).fetchall()
        if len(self.book) == 0:
            return False
        else:
            # return(self.book[0])
            self.book_title = self.book[0][2]
            self.book_author = self.book[0][3]
            self.book_year = self.book[0][4]

            #getting information from another api
            self.get_rating = GetRatings(self.isbn)
            self.review_rating = self.get_rating.ratings()
            self.review_count = self.review_rating[0]
            self.average_score = self.review_rating[1]

            return (self.book_title,self.book_author,self.book_year,self.review_count,self.average_score)

            