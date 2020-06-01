import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests



app = Flask(__name__)

app.config['DATABASE_URL']='postgres://jygfjdwhtrewcg:55eb38717969d43f3a4f3a452753e57ac586409b72f7e9df58d79f963db1e466@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dcb1fa3mhsek6f'

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
    return render_template("homepage.html", work=work)


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

@app.route("/logout", methods=["POST"])
def logout():
    return render_template("logout.html")

