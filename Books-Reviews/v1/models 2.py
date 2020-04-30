from flask_sqlalchemy import SQLAlchemy
import datetime

#creating an instance of SQLAlchemy
db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String, nullable=False)
    book_title = db.Column(db.String, nullable=False)
    book_author = db.Column(db.String, nullable=False)
    book_year_published = db.Column(db.String, nullable=False)

class Users(db.Model):
    __tablename__ = "user_credentials"
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)

    def addUser(self, fname, lname, phone_number, country, province, city, postal_code):
        db.execute("INSERT into user_data(user_id,user_first_name,user_last_name,user_phone_number,user_country,user_province,user_city,user_postal_code) VALUES(:user_id,:fname,:lname,:phone_number,:country,:province,:city,:postal_code)", {"user_id":self.id,"fname":fname,"lname":lname,"phone_number":phone_number,"country":country,"province":province,"city":city,"postal_code":postal_code})
        db.commit()

class User_Data(db.Model):
    __tablename__ = "user_data"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_credentials.id"), nullable=False)
    user_first_name = db.Column(db.String, nullable=False)
    user_last_name = db.Column(db.String, nullable=False)
    user_phone_number = db.Column(db.String, nullable=False)
    user_country = db.Column(db.String, nullable=False)
    user_province = db.Column(db.String, nullable=False)
    user_city = db.Column(db.String, nullable=False)
    user_postal_code = db.Column(db.String, nullable=False)

class Reviews(db.Model):
    __tablename__ = "book_reviews"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_credentials.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    book_review = db.Column(db.String, nullable=False)