import os
from flask import Flask, render_template, redirect, request, url_for, request, flash, session
import dns
from flask-mail import Mail, Message
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from wtforms import StringField, TextField, SubmitField, PasswordField, ValidationError
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from forms import RegForm
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)

# MongoEngine setup
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGODB_HOST"] = os.environ.get("MONGODB_HOST")
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
db = MongoEngine(app)

# Flask Login setup
login_manager = LoginManager(app)

# This callback exists as part of the flask-login auth process.


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

# Flask-Mail setup variables


app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

msg = Message()

# Routes below this point


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


# Flask-Login compliant registration scheme.

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(
                    form.password.data, method='sha256')
                new_user = User(email=form.email.data,
                                password=hashpass).save()
                login_user(new_user)
                flash("Login succesful!")
                return redirect(url_for('profile'))
            else:
                flash("Email already registered!")
        else:
            flash("Improper registration! This error means your form was not validated.")
    return render_template('register.html', form=form)

# Flask-Login compliant login


@app.route('/login', methods=["GET", "POST"])
def login():
    # First check to see if user is already logged in.
    if current_user.is_authenticated == True:
        return redirect(url_for('profile'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            # First of all, check if there is a registered email in the DB that matches.
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                # If email matches an entry, check the password hash.
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('profile'))
            else:
                flash("The email entered does not appear to be registered!")
    return render_template('login.html', form=form)

# Profile page


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")

# Route for creating new entries


@app.route('/profile/addchar', methods=["GET", "POST"])
def addchar():
    return render_template("addchar.html")

# Route for lost-password request form


@app.route('/lost_password', methods=["GET", "POST"])
def lost_password():
    form = LostPass()
    return render_template("lost_password.html", form=form)


# Logout function + redirect


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)
