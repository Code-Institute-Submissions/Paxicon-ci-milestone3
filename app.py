import os
from flask import Flask, render_template, redirect, request, url_for, request, flash, session
import dns
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/characters")
def characters():
    chars_sheets = []
    chars = mongo.db.char_sheets.find()

    for i in chars:
        chars_sheets.append(i)
    return render_template("characters.html", characters=chars_sheets)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/lore')
def lore():
    return render_template("lore.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration succesful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check for user in DB records
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # If existing user, check password.
        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                flash("Username and/or password incorrect.")
                return redirect(url_for("login"))
        else:
            # Password check failed
            flash("Username and/or password incorrect.")
            return redirect(url_for("login"))

    return render_template("login.html")

# Profile page


@app.route('/profile/<username>', methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=session["user"])

# Logout function + redirect


@ app.route('/logout')
def logout():
    flash("You have been logged out!")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)
