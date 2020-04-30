from flask_sqlalchemy import SQLAlchemy
import datetime

#creating an instance of SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    #book_id = db.Column(db.String, db.ForeignKey("books.id"), nullable=False)
