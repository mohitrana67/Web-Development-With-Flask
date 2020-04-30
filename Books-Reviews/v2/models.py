from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#Set up database
engine = create_engine("postgres://pvvjoazaealpqs:4d4ce3e1d242705bfd1904bf5edff3e88437f8135c9b0be9b07e2f9df4468948@ec2-54-83-202-132.compute-1.amazonaws.com:5432/d9i9akof301l1j")
db = scoped_session(sessionmaker(bind=engine))

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