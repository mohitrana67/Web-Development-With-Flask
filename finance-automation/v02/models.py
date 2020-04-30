from flask_sqlalchemy import SQLAlchemy
import datetime

#creating an instance of SQLAlchemy


# Set up database

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "user_credentials"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.)
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