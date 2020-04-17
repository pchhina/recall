from flask import Flask, redirect, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


# Configure application
app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect("recall.db", check_same_thread=False)
db = conn.cursor()

# Wish List 

# str str -> insert into db
# registers a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        pwd = request.form.get("pwd")
        pwd2 = request.form.get("pwd2")
        print(name, pwd, pwd2)
        pwd_hash = generate_password_hash(pwd)
        ins = "INSERT INTO users (username, hash) VALUES (?, ?)"
        conn.execute(ins, (name, pwd_hash))
        conn.commit()
        return redirect("/")

# str str -> check db
# login a user
@app.route("/login")
def login():
    return render_template("login.html")

# str str -> insert into db
# adds a question-answer to db
@app.route("/add")
def add():
    return render_template("add.html")

# 
# starts a test
@app.route("/test")
def test():
    return render_template("test.html")

# 
# shows user statistics
@app.route("/stats")
def stats():
    return render_template("stats.html")

#
# renders home page on application launch
@app.route("/")
def index():
    return render_template("index.html")
