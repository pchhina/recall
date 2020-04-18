from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required
from flask_session import Session
from tempfile import mkdtemp
import sqlite3


# Configure application
app = Flask(__name__)

### (DON'T UNDERSTAND YET) ###
# Ensure templates are auto-reloaded 
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

### (END DON'T UNDERSTAND YET) ###

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
        db.execute(ins, (name, pwd_hash))
        conn.commit()
        return redirect("/login")

# str str -> check db
# login a user
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        name = request.form.get("username")
        pwd = request.form.get("pwd")

        # Query database for username
        sel ="SELECT * FROM users WHERE username = ?"
        db.execute(sel, (name,))
        rows = db.fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][2], pwd):
            return render_template("apology.html", msg='''username does not
                    match''', code=403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        return redirect("/")

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
@login_required
def index():
    db.execute("SELECT username FROM users WHERE id = ?",
            (session["user_id"],))
    rows = db.fetchall()
    name = rows[0][0]
    return render_template("index.html", name=name)
