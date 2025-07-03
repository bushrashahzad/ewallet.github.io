import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route("/summary",methods=["GET", "POST"])
@login_required
def summary():
    spends = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
    total_s = 0
    for i in spends:
        total_s += i['spend2']
    db.execute("UPDATE users SET spend1 = ? WHERE id = ?", total_s, session['user_id'])
    total_s1 = db.execute("SELECT spend1 FROM users WHERE id = ?", session["user_id"])
    cash10 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    monthly1 = db.execute("SELECT * FROM monthly WHERE id = ?", session["user_id"])
    return render_template("list.html", total_s1=total_s1, cash10=cash10, monthly1=monthly1)

@app.route("/monthly", methods=["GET", "POST"])
@login_required
def monthly():
    if request.method == "POST":
        now = datetime.now()
        datetime1 = now.strftime("%Y/%m/%d %H:%M:%S")
        db.execute("INSERT INTO monthly (id, homerent, groceries, eb, shopping, other, datetime, travel, petrol, loan, education, weekly) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], request.form.get("homerent"), request.form.get("groceries"), request.form.get("eb"), request.form.get("shopping"), request.form.get("other"), datetime1, request.form.get("travel"), request.form.get("petrol"), request.form.get("loan"), request.form.get("education"), request.form.get("weekly"))
        add = db.execute("SELECT spend2, homerent, groceries, eb, shopping, other, travel, petrol, loan, education, weekly FROM monthly WHERE id = ?", session["user_id"])
        total = 0
        for i in add:
            i['spend2'] += i['homerent']
            i['spend2'] += i['groceries']
            i['spend2'] += i['eb']
            i['spend2'] += i['shopping']
            i['spend2'] += i['other']
            i['spend2'] += i['travel']
            i['spend2'] += i['petrol']
            i['spend2'] += i['loan']
            i['spend2'] += i['education']
            i['spend2'] += i['weekly']
        total += i['spend2']
        db.execute("INSERT INTO sum (spend2, user_id) VALUES (?, ?)", i['spend2'], session["user_id"])
        m = db.execute("SELECT monthly_id FROM monthly WHERE id = ?", session["user_id"])
        for i in m:
            session["monthly_id"] = i["monthly_id"]
        db.execute("UPDATE monthly SET spend2 = ? WHERE id = ? and monthly_id = ?", total, session["user_id"], session["monthly_id"])
        cash0 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if cash0[0]['cash'] == 0:
           cash0[0]['cash'] = 0
        else:
            s = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
            for i in (s):
                cash12 = cash0[0]['cash'] - i['spend2']
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash12, session["user_id"])
        return redirect("/summary")
    return render_template("buy.html")

@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    if request.method == "POST":
        income = int(request.form.get("income"))
        cash1 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash2 = cash1[0]['cash']
        cash2 += income
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash2, session["user_id"])
        now = datetime.now()
        datetime3 = now.strftime("%Y/%m/%d %H:%M:%S")
        db.execute("INSERT INTO income (user_id, income1, datetime5) VALUES (?, ?, ?)", session["user_id"], income, datetime3)
        cash0 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        s = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
        if cash0[0]['cash'] == 0:
           cash0[0]['cash'] = 0
        else:
            spends = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
            total_s2 = 0
            for i in spends:
                total_s2 += i['spend2']
            cash12 = cash0[0]['cash'] - total_s2
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash12, session["user_id"])
    income3 = db.execute("SELECT * FROM income WHERE user_id = ?", session["user_id"])
    return render_template("income.html", income3=income3)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", msg="invalid username/password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    if request.method == "POST":

        if not confirmation in password:
            return render_template("register.html", msg="The password don't match")

        all_users = db.execute("SELECT username FROM users;")

        for i in range(len(all_users)):
            if username == all_users[i]["username"]:
                return render_template("register.html", msg="Sorry, username has taken!")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        return redirect("/")
    
    return render_template("register.html")
