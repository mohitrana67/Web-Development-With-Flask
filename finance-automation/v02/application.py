import os
import hashlib, binascii, os


from flask import Flask, session, render_template, request, redirect, url_for, g, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model import *
from datetime import datetime

app = Flask(__name__)

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
app.secret_key = os.urandom(24) 

# Set up database
# engine = create_engine("postgres://aagwkpzqcmjlcp:632797451d6b8c816f564ec9fe08df08ae1278b0d106c5ef0d19649f7db45231@ec2-174-129-33-156.compute-1.amazonaws.com:5432/deln6atfh1l79a")
# db = scoped_session(sessionmaker(bind=engine))

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
                now = datetime. now()
                user_loged_in_time = now. strftime("%H:%M:%S")
                session[username] = [fname,lname,user_loged_in_time]

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
        password = str(request.form.get("user_password"))
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
                stored_password = users.select(username,1)[2]
                # return (hashed_password)
                #matching the passwords
                verify_hashed_password = verify_password(stored_password, password)

                # verify_password = (hashed_password == password)

                # we need to change this code to work fro Trues statement
                if verify_hashed_password == False:
                    user_data = users.select(username,2)
                    fname = user_data[0]
                    lname = user_data[1]
                    session[username] = [fname,lname]
                    return redirect(url_for('profile', user=username))
                else:
                    return render_template("login.html", message_login = "Please enter correct username and password")
    else:
        # We have to implement user to not get login page again if he already is logged in
        # return session.get('username')
        return render_template("login.html")

# route for creating a profile
@app.route("/profile/<user>")
def profile(user):
    if user in session:
        # return "You are here"
        return render_template("profile.html",username=user)
    else:
        return "Please login again"

# get information about expenses last year
@app.route("/finance/<year>", methods=["GET"])
def finance(year):
    data = {
        'hello' : 'world',
        'number' : 4
    }
    js= jsonify(data)
    return(js)

# logout rouite for loggin out of the session
@app.route("/logout/<user>")
def logout(user):
    session.pop(user)
    return redirect(url_for('index'))

# killing all the sessions at time
@app.route("/killall")
def killall():
    session.clear()
    return "Cleared"

@app.route('/uploadfile/<user>', methods=["POST"])
def upload_data(user):
    if request.method == 'POST':
        # return user
        # Create variable for uploaded file
        f = request.files['file']  

        if not f:
            return "No file"
        else:
            readCSV = CSV(f,1)

        uploadedFile = readCSV.read_csv_with_filelocation()

        return render_template("profile.html", username=user, uploadedFile = uploadedFile)

        # return redirect(url_for('profile', user=user, uploadedFile = uploadedFile))

if __name__ == "__main__":
    app.run(debug=True)