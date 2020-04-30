import os
import hashlib, binascii, os

from flask import Flask, session, render_template, request, redirect, url_for, g
from models import *

app = Flask(__name__)

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


@app.route("/")
def index():
    return render_template("index.html")

#route for registeratio
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
        
        if len(username) == 0:
            return render_template("register.html", message_registeration = "Please enter a valid username")
        elif len(password) == 0:
            return render_template("register.html", message_registeration = "Please enter a valid password")
        else:
            #password is hashed using the hash function in python
            hashed_password = hash_password(password)

            #searching for whether the username already exists or not
            user_rowcount = db.execute("SELECT * FROM user_credentials WHERE user_username = :user_username", {"user_username": username}).rowcount

            if user_rowcount == 0:
                #adding data to the user_credential table
                db.execute("INSERT into user_credentials(user_username, user_password) VALUES(:user_username, :user_password)",{"user_username":username, "user_password":hashed_password})
                db.commit()
                #adding data to user_Data table
                #getting user_id
                user_id = db.execute("SELECT id from user_credentials WHERE user_username=:username_name",{"username_name":username}).fetchone()
                #adding user_credentials
                db.execute("INSERT into user_data(user_id,user_first_name,user_last_name,user_phone_number,user_country,user_province,user_city,user_postal_code) VALUES(:user_id,:fname,:lname,:phone_number,:country,:province,:city,:postal_code)", {"user_id":user_id[0],"fname":fname,"lname":lname,"phone_number":phone_number,"country":country,"province":province,"city":city,"postal_code":postal_code})
                db.commit()
                session[username] = [fname,lname]
                return redirect(url_for('profile', user=username))
            else:
                return render_template("register.html", message_registeration = "Please choose some other user email")
    else:
        return render_template("register.html")
