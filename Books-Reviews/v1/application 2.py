import os
import hashlib, binascii, os

from flask import Flask, session, render_template, request, redirect, url_for, g, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from allsql import *
from goodpress import *

app = Flask(__name__)

# Check for environment variable
#if not os.getenv("postgres://pvvjoazaealpqs:4d4ce3e1d242705bfd1904bf5edff3e88437f8135c9b0be9b07e2f9df4468948@ec2-54-83-202-132.compute-1.amazonaws.com:5432/d9i9akof301l1j"):
#    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#hashing the passwod
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

#unhashing the password and check
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# Set up database
engine = create_engine("postgres://pvvjoazaealpqs:4d4ce3e1d242705bfd1904bf5edff3e88437f8135c9b0be9b07e2f9df4468948@ec2-54-83-202-132.compute-1.amazonaws.com:5432/d9i9akof301l1j")
db = scoped_session(sessionmaker(bind=engine))

#route for home page
@app.route("/")
def index():
    return render_template("index.html")

#route for registeration
@app.route("/register", methods=["GET","POST"])
def register_user():
    if request.method == "POST":
        #getting user data from the request 
        username = request.form.get("user_username")
        password = request.form.get("user_password")
        fname = request.form.get("user_first_name")
        lname = request.form.get("user_last_name")
        phone_number = request.form.get("user_phone_number")
        country = request.form.get("user_country")
        province = request.form.get("user_province")
        city = request.form.get("user_city")
        postal_code = request.form.get("user_postal_code")
        users = Users()
        
        if len(username) == 0:
            return render_template("register.html", message_registeration = "Please enter a valid username")
        elif len(password) == 0:
            return render_template("register.html", message_registeration = "Please enter a valid password")
        else:
            #password is hashed using the hash function in python
            hashed_password = hash_password(password)

            #searching for whether the username already exists or not 
            user_found = users.select(username,0)
            # return str(is_user_available)

            if user_found == False:
                #adding data to the user_credential table
                users.insert_user_credentials(username,hashed_password,fname,lname,phone_number,country,province,city,postal_code)
                
                #adding user into session
                session[username] = [fname,lname]

                # redirecting user to the profile page
                return redirect(url_for('profile', user=username))

            elif user_found == True:
                # returing user to the register page stating an error message
                return render_template("register.html", message_registeration = "Please choose some other user email")
    else:
        return render_template("register.html")

#route for login
@app.route("/login", methods=["POST","GET"])
def login_user():
    if request.method == "POST":
        #getting user data from the request 
        username = request.form.get("user_username")
        password = request.form.get("user_password")
        if len(username) == 0:
            return render_template("login.html", message_login = "Please enter a valid username")
        elif len(password) == 0:
            return render_template("login.html", message_login = "Please enter a valid password")
        else:
            users = Users()
            user_found = users.select(username,0)
            if user_found == False:
                return render_template("login.html", message_login = "Please check you username as we dont have any user with this username")
            elif user_found == True:
                hashed_password = users.select(username,1)[2]

                #matching the passwords
                verify_hashed_password = verify_password(hashed_password, password)

                if verify_hashed_password == True:
                    session[username] = [username]
                    return redirect(url_for('profile', user=username))
                else:
                    return render_template("login.html", message_login = "Please enter correct username and password")
    else:
        return render_template("login.html")

#route for creating a profile
@app.route("/profile/<user>")
def profile(user):
    if user in session:
        return render_template("profile.html",username=user)
    else:
        return "Please login again"

#route for searching a book
@app.route("/search/<user>", methods=["POST","GET"])
def search_books(user):
    if user in session:
        if request.method == "POST":
            attribute = request.form.get("attribute")
            final_attribute = attribute+ "%"
            books = db.execute("SELECT * from books where book_title like :attribute OR book_author like :attribute OR book_isbn like :attribute",{"attribute":final_attribute}).fetchall()

            if len(books) == 0:
                return render_template("profile.html", username=user, error_message="Nothing to display")
            else:
                return render_template("profile.html", username=user, books=books)
        else:
            return render_template("profile.html", username=user)
    else:
        return "Please login before accessing this page"

#route for displaying inforamtion about every book
@app.route("/books/<user>/<book_id>")
def books(user,book_id):
    username = user
    book_id = book_id

    book = Book(book_id,user)
    book_details = book.select()
    goodpress = GetRatings(str(book_details[2]))
    get_ratings = goodpress.ratings()
    total_reviews = str(get_ratings[0])
    average_rating = str(get_ratings[1])

    if username in session:
        return render_template("books.html", user=username, book_isbn=book_details[2],book_title=book_details[0], book_author=book_details[1], book_year=book_details[3], book_id = book_id, total_reviews = total_reviews,average_rating = average_rating)
    else:
        return "Please login to view this page"

#route for adding the reviews to the book
@app.route("/add_review/<user>/<book_id>", methods=["POST","GET"])
def add_reviews(user,book_id):
    if user in session:
        book = Book(book_id,user)
        book_details = book.select()
        if request.method == "POST":
            #return book_id
            review = request.form.get("review")
            rating = request.form["rating"]
            #return "You are in adding review block"
            is_review_available = str(book.check_previous_review())
            # return result
            if is_review_available == 'True':
                return render_template("books.html", user=user, book_id=book_id, book_title = book_details[0], book_author = book_details[1], book_isbn = book_details[2],error_message = "You already posted a review")
            else:
                if len(review) == 0:
                    return render_template("books.html", user=user, book_id=book_id, error_message="This is not true")
                else:   
                    book.add_review(review,rating)
                    return render_template("books.html", user=user, book_id=book_id, book_title = book_details[0], book_author = book_details[1], book_isbn = book_details[2],review=review, success_message = "review added")
        else:
            return render_template("books.html", user=user, book_id=book_id, book_title = book_details[0], book_author = book_details[1], book_isbn = book_details[2])
    else:
        return "Please login before using this page"

@app.route("/logout/<user>")
def logout(user):
    session.pop(user)
    return redirect(url_for('index'))

@app.route("/killall")
def killall():
    session.clear()
    return "Cleared"

#route for api creation
@app.route("/api/<int:book_isbn>")
def book_api(book_isbn):
    """Return Information about different books on the basis of the book isbn"""

    # return "You are in api folder"
    #make sure book with that isbn exists
    api = API()
    result = api.search_by_isbn(book_isbn)
    if result is False:
        return jsonify({"error": "Invalid book ISBN"}), 404
    else:
        api = API()
        result = api.search_by_isbn(book_isbn)
        # return str(result)
        return jsonify({
            "title": result[0],
            "author": result[1],
            "year": result[2],
            "isbn": book_isbn,
            "review_count":result[3],
            "average_score":result[4]
        })
    
if __name__ == "__main__":
    app.run(debug=True)