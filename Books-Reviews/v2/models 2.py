import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "user_credentials"
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    