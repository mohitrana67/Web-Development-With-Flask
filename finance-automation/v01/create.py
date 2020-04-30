from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://aagwkpzqcmjlcp:632797451d6b8c816f564ec9fe08df08ae1278b0d106c5ef0d19649f7db45231@ec2-174-129-33-156.compute-1.amazonaws.com:5432/deln6atfh1l79a"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()