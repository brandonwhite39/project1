import os

from flask import Flask, session, render_template, request, jsonify
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

user_id=""
uid=0

@app.route("/")
def index():
    test = db.execute("SELECT * FROM books").fetchone()
    work = test['isbn']
    return render_template("homepage.html", work=work)


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/created", methods=["POST"])
def created():
    user = request.form.get("username")
    
    password = request.form.get("password")
    db.execute("INSERT INTO users (username, password) VALUES (:user, :password)",
               {"user":user, "password":password})
    db.commit()
    return render_template("success.html", user=user, password=password)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
    username = request.form.get("username")
    password = request.form.get("password")
    global user_id
    global uid
    userID = db.execute("SELECT id FROM users WHERE username=:username",
                        {"username":username}).fetchone()
    uid = userID
    user_id = username
    if db.execute("SELECT * FROM users WHERE username=:username AND password=:password",
                  {"username":username, "password":password}).rowcount == 0:
        return render_template("error.html",
                               message="Not a valid username/password combination.")
    else:
        return render_template("home.html",
                               username=username, password=password, uid=uid)

@app.route("/mainpage", methods=["POST"])
def mainpage():
    return render_template("mainpage.html")

@app.route("/search", methods=["POST"])
def search():
    search = request.form.get("search")
    #check if inputted characters give back a result
    if db.execute("SELECT * FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search",
                  {"search": '%{}%'.format(search)}).rowcount == 0:
        return render_template("error.html", message="No valid entries.")
    else:
        result = db.execute("SELECT * FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search",
                            {"search": '%{}%'.format(search)}).fetchall()
        return render_template("search.html", result=result, uid=uid)

@app.route("/search/<isbn>") #add back post method for accessing
def bookpage(isbn):
    title = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn})
    reviews = db.execute("SELECT * FROM review WHERE isbn=:isbn", {"isbn":isbn})
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "wJMCIDlviRcrcAOUacnHwQ", "isbns": isbn})
    return render_template("bookpage.html", isbn=isbn, title=title, reviews=reviews, res=res.json())

@app.route("/search/<isbn>/review")
def review(isbn):
    title = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn})
    currentUser = user_id
    
    return render_template("review.html", isbn=isbn, title=title, currentUser=currentUser)

@app.route("/search/<isbn>/review/success", methods=["POST"])
def success(isbn):
    currentUser = user_id
    userID = uid[0]
    review = request.form.get("reviewcontent")
    rating = request.form.get("rating")
    row = db.execute("SELECT * FROM review WHERE isbn=:isbn AND id=:userID",
                         {"isbn":isbn, "userID":userID})
    rowcount=row.rowcount
    if rowcount==1:
        return render_template("error.html", message="Already submitted a review!")
    if review=="" and rating==None:
        #no info added
        return render_template("error.html", message="No review content.")
    elif review=="" and rating!=None:
        #rating inputted, no review text
        db.execute("INSERT INTO review (isbn, rating) VALUES (:isbn, :rating)",
                   {"isbn": isbn, "rating": rating})
        db.commit()
        return render_template("successreview.html", isbn=isbn, rating=rating)
    elif review!="" and rating==None:
        #rating not given, review inputted
        db.execute("INSERT INTO review (isbn, comments) VALUES (:isbn, :review)",
                   {"isbn": isbn, "review": review})
        db.commit()
        return render_template("successreview.html", isbn=isbn, review=review, uid=uid)
    else:
        #rating and review given
        db.execute("INSERT INTO review (isbn, rating, comments, id) VALUES (:isbn, :rating, :review, :userID)",
                       {"isbn": isbn, "rating": rating, "review":review, "userID":userID})
        db.commit()
        
        return render_template("successreview.html", isbn=isbn, review=review, rating=rating, rowcount=rowcount)
        
    
@app.route("/api/<isbn>", methods=["GET"])
def json(isbn):
    
    if db.execute("SELECT isbn FROM books WHERE isbn=:isbn", {"isbn":isbn}).rowcount == 0:
        return jsonify({"error": "Invalid isbn number"}), 404
    else:
        bookinfo = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "wJMCIDlviRcrcAOUacnHwQ", "isbns": isbn})
        resjson = res.json()
        return jsonify({
            "title": bookinfo.title,
            "author": bookinfo.author,
            "year": bookinfo.year,
            "isbn": bookinfo.isbn,
            "review_count": resjson["books"][0]["reviews_count"],
            "average_score": resjson["books"][0]["average_rating"]
            })


@app.route("/logout", methods=["POST"])
def logout():
    return render_template("logout.html")

