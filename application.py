from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Wish List 

# str str -> insert into db
# registers a new user
@app.route("/register")
def register():
    return render_template("register.html")

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
