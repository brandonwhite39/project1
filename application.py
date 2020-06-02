import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "wJMCIDlviRcrcAOUacnHwQ", "isbns": "9781632168146"})

@app.route("/")
def index():
    test = db.execute("SELECT * FROM books").fetchone()
    work = test['isbn']
    return render_template("homepage.html", work=work, res=res.json())


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/created", methods=["POST"])
def created():
    return render_template("success.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    search = request.form.get("search")
    #check if inputted characters give back a result
    if db.execute("SELECT * FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search", {"search": '%{}%'.format(search)}).rowcount == 0:
        return render_template("error.html", message="No valid entries.")
    else:
        result = db.execute("SELECT * FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search", {"search": '%{}%'.format(search)}).fetchall()
        return render_template("search.html", result=result)

@app.route("/search/<isbn>") #add back post method for accessing
def bookpage(isbn):
    title = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn})
    return render_template("bookpage.html", isbn=isbn, title=title)

@app.route("/search/<isbn>/review")
def review(isbn):
    title = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn})
    #need to show the reviews that have been made for book already on webpage
    return render_template("review.html", isbn=isbn, title=title)

@app.route("/search/<isbn>/review/success", methods=["POST"])
def success(isbn):
    review = request.form.get("reviewcontent")
    rating = request.form.get("rating")
    #using isbn forsure, need to check if reviewcontent is empty and/or rating is empty
    #should include some sort of message saying if stored and what has been stored.
    
    return render_template("successreview.html", isbn=isbn, review=review, rating=rating)

@app.route("/logout")
def logout():
    return render_template("logout.html")

