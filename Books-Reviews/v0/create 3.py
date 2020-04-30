from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://pvvjoazaealpqs:4d4ce3e1d242705bfd1904bf5edff3e88437f8135c9b0be9b07e2f9df4468948@ec2-54-83-202-132.compute-1.amazonaws.com:5432/d9i9akof301l1j"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()