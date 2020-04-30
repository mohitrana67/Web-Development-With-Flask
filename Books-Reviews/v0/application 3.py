from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

#@app.route("/<string:name>")
#def hello(name):
#    return f"Hello, {name}"

@app.route("/")
def index():
    headline_app = "This is the headline for today and this is to check the deugger mode"
    # giving a parameter to the index.html so that headline variable can be used anywhere in tha index.html page
    return render_template("index.html", headline = headline_app)

@app.route("/bye")
def bye():
    headline_app = "Good Bye"
    return render_template("index.html", headline = headline_app)

@app.route("/isNewYear")
def isDateTime():
    now = datetime.datetime.now()
    #we are checking if the month and the day are as followed
    new_year = now.month == 10 and now.day == 27
    return render_template("index.html", is_new_year = new_year, new_year = now)

@app.route("/list")
def lists():
    names = ["Mohit","Rohit","Sachin","Ayush","Nishant","Neha"]
    return render_template("index.html", names = names)

@app.route("/expense", methods=["GET", "POST"])
def expense():
    if request.method == "GET":
        return render_template("expense.html")
    else:
        name = request.form.get("name")
        return render_template("index.html", name=name)

if __name__ == "__main__":
    app.run()
