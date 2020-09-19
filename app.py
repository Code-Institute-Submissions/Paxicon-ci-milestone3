import os
from flask_jwt import jwt, jwt_required
import datetime
from flask import Flask, render_template, redirect, request, url_for, request, flash, session
import dns
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from wtforms import StringField, TextField, SubmitField, PasswordField, ValidationError
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from forms import RegForm, LostPass
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
# This callback exists as part of the flask-login auth process.
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

# Flask-Mail setup variables


app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
mail = Mail(app)

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
                    form.password.data)
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

# Flask-Login compliant login, with password-reset functionality


@app.route('/login', methods=["GET", "POST"])
def login():
    # First check to see if user is already logged in.
    if current_user.is_authenticated == True:
        return redirect(url_for('profile'))
    form = RegForm()
    password = form.password.data
    if request.method == 'POST':
        # First of all, check if there is a registered email in the DB that matches.
        check_user = User.objects(email=form.email.data).first()
        if check_user is None:
            # If no matching user is found, inform the user.
            flash("The email entered does not appear to be registered!")
        else:
            # If email matches an entry, check the password hash.
            if check_password_hash(check_user['password'], password):
                login_user(check_user)
                return redirect(url_for('profile'))
            else:
                flash("Invalid credentials")
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
    # Password Reset functionality
    if request.method == 'POST':
        if form.validate():
            # First of all, check if there is a registered email in the DB that matches.
            check_user = User.objects(email=form.email.data).first()
            # Checking if this e-mail exists in the database. If not, flashes an error to the user.
            if check_user:
                email = str(form.email.data)
                exp_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                # If a user is found, we'll proceed to generate a JWT-token to pass along with our mail.
                token = jwt.encode({'reset_password': form.email.data,
                                    'exp': exp_time},
                                   key=os.getenv('SECRET_KEY'))
                password_mail = Message("Lost your password?",
                                        sender=os.environ['MAIL_USERNAME'],
                                        recipients=[email],
                                        html=render_template('reset_email.html', token=token))
                mail.send(password_mail)
                # Feedback so the user can see the request went through!
                flash(
                    "Reset password email sent to the provided email! Please check your email and follow instructions therein.")
            else:
                flash("No such user found!")

    return render_template("lost_password.html", form=form)


@app.route("/mail_verified/<token>",  methods=['GET', 'POST'])
def mail_verified(token):

    # This form does not use the FlaskForm-extension. This is because of a bug with validation that made the JWT-token invalid and the form would not validate correctly,
    # causing faulty passwords to be saved.

    user = jwt.decode(token, key=os.getenv('SECRET_KEY'))["reset_password"]
    token_valid = User.objects(email=user).first()
    password = request.form.get("password")
    # Verified the token is still valid.
    if request.method == 'POST':
        # If a post occurs, check the validity of the token against the DB of registered users.

        if token_valid is None:
            flash("Invalid token, password reset request denied.")
            return redirect(url_for('login'))
        else:

            # If a token matching the JWT-token payload has been found, hash the current input and save it to the database.

            token_valid.password = generate_password_hash(password)
            token_valid.save().reload()

            flash("Your password has been changed!")
            login_user(token_valid)
            return redirect(url_for('profile'))
    return render_template('verified_password_change.html', token=token)


@ app.route('/logout', methods=['GET'])
@ login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)
