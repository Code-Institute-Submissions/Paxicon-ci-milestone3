import os
from flask_jwt import jwt
import datetime
from flask import Flask, render_template, redirect, request, url_for, request, flash, jsonify, session
import dns
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine, Document
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from wtforms import StringField, TextField, SubmitField, PasswordField, ValidationError
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from charsheets import Char, CharInput
from forms import RegForm, LostPass, MailMeForm
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

# Flask-Mail config variables.


app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
mail = Mail(app)

# Routes below this point.


@app.route('/')
def home():
    return render_template("home.html")

# Grabs all contents of the Char collection from the DB, orders it alphabetically and feeds it into characters.html for rendering.


@app.route("/characters")
def characters():
    all_characters = Char.objects().order_by('content.Name')

    return render_template("characters.html", all_characters=all_characters)

# Renders about.html and, if post, validates the form, submits it and sends it using the Flask-Mail extension.


@ app.route('/about', methods=["GET", "POST"])
def about():
    form = MailMeForm()
    # Handler for the MailMe modal.
    if request.method == 'POST':
        form_data = form.data
        if form.validate_on_submit():
            contact_mail = Message(subject=str(form.subject.data),
                                   sender=os.environ['MAIL_USERNAME'],
                                   recipients=[
                'test-account@patrikaxelsson.one'],
                html=render_template('contact_mail.html', form_data=form_data))
            mail.send(contact_mail)
            # Feedback so the user can see the request went through.
            flash(
                "Your message has been sent! We'll get back to you as soon as possible!")
            # Redirect back to 'about' to reset the form and show the flash.
            return redirect(url_for('about'))
    return render_template("about.html", form=form)

# Flask-Login compliant user registration scheme.


@ app.route('/register', methods=["GET", "POST"])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(
                    form.password.data)
                new_user = User(display_name=form.display_name.data,
                                email=form.email.data,
                                password=hashpass).save()
                login_user(new_user)
                flash("Login succesful!")
                return redirect(url_for('profile'))
            else:
                flash("Email already registered!")
        else:
            flash("Improper registration! This error means your form was not validated.")
    return render_template('register.html', form=form)

# Flask-Login compliant login system, When posting, uses werkzeug to check the password hash against the User collection of the DB.


@ app.route('/login', methods=["GET", "POST"])
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


@ app.route('/profile', methods=["GET", "POST"])
@ login_required
def profile():
    # This definition of user is the best for our purposes
    form = RegForm()
    user = current_user.get_id()
    MyChars = Char.objects(Owner=user)

    # Handler for account-deletion, checks password and flashes the user a confirmation modal informing them all characters they've added will also be deleted.
    if request.method == 'POST':
        if check_password_hash(current_user['password'], form.password.data):
            flash("Your account has been deleted.")
            User.objects(id=user).first().delete()
            return redirect(url_for('home'))
        else:
            flash(
                "You have supplied invalid credentials and have been logged out for account security reasons.")
            logout_user()
            return redirect(url_for('home'))

    return render_template("profile.html", Chars=MyChars, form=form, user=current_user)

# The following route is for allowing users to delete their characters from the database. The "GET" only serves a redirect to the main profile, the route is there only to
# handle forms.


@ app.route('/profile/del_char/<char_id>', methods=["GET", "POST"])
@ login_required
def del_char(char_id):
    character = Char.objects(pk=char_id).first()
    if request.method == 'POST':
        character.delete()
        flash("Character deleted!")
        return redirect(url_for('profile'))

    return redirect(url_for('profile'))

# This route is another subsection of the profile-page. Like the one above, it exists only to process requests to MongoEngine for the user to change their display-name and redirects to Profile otherwise.


@ app.route('/profile/updt_name/<user_id>', methods=["GET", "POST"])
@ login_required
def updt_name(user_id):
    newName = request.form["display_name"]
    user = User.objects(pk=user_id).first()
    if request.method == 'POST':
        user.update(display_name=newName)
        user.save().reload()
        flash("Your display name has been changed!")

    return redirect(url_for('profile'))

# Route for creating new entries in the character database.


@ app.route('/profile/addchar', methods=["GET", "POST"])
@ login_required
def addchar():
    form = CharInput()
    check_user = User.objects(email=current_user.email).first()
    form_data = form.data
    if request.method == 'POST' and form.validate():
        # First we need to prepare a new Char object
        new_char = Char()
        # Char() is a dynamic document class, so we can easily insert the full form data-dump, while keeping the object-ID of the owner easily accessible for queries.
        # Note: This adds all form-data submitted as a nested object inside the document.
        new_char.content = form_data
        # Owner tags against the currently logged in user, gets the object-ID of their User account, then applies it under the key of "Owner" to the new entry. This allows
        # us to specify cascading deletion rules, so there are no dangling references to deleted accounts.
        new_char.Owner = check_user
        new_char.save()
        flash("New character added!")
        return redirect(url_for('profile'))

    return render_template("addchar.html", form=form)

# Route for lost-password request form


@ app.route('/lost_password', methods=["GET", "POST"])
def lost_password():
    form = LostPass()
    # Password Reset functionality
    if request.method == 'POST':
        if form.validate():
            # First of all, check if there is a registered email in the DB that matches.
            # Checking if this e-mail exists in the database. If not, flashes an error to the user.
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                # If a user is found, we'll proceed to generate a JWT-token to pass along with our mail.
                email = str(form.email.data)
                exp_time = datetime.datetime.now() + datetime.timedelta(hours=1)
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
                flash("No user found!")

    return render_template("lost_password.html", form=form)


@ app.route("/mail_verified/<token>",  methods=['GET', 'POST'])
def mail_verified(token):

    # This form does not use the FlaskForm-extension. This is because of a bug with validation that made the JWT-token invalid and the form would not validate correctly,
    # causing faulty passwords to be saved to the database. Security is instead provided by the URL being passed to the users external email inbox, proving they are the owner
    # of the account.

    # Verified the token is still valid, by decrypting it and checking it against the database to see if the decrypted token matches a user
    user = jwt.decode(token, key=os.getenv('SECRET_KEY'))["reset_password"]
    token_valid = User.objects(email=user).first()
    password = request.form.get("password")

    if request.method == 'POST':
        # If a post occurs, check the validity of the token against the DB of registered users.

        if token_valid is None:
            # This route triggers if the token is expired or otherwise faulty and redirects to the login page. Legitimate users can from there request a new reset-email.
            flash("Invalid token, password reset request denied.")
            return redirect(url_for('login'))
        else:
            # If a token matching the JWT-token payload has been found, we hash  the current input and save it to the database.
            token_valid.password = generate_password_hash(password)
            token_valid.save().reload()
            # User feedback and redirect
            flash("Your password has been changed!")
            login_user(token_valid)
            return redirect(url_for('profile'))
    return render_template('verified_password_change.html', token=token)

# Route for logging users out of the app.


@ app.route('/logout', methods=['GET'])
@ login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Char-Profile is the actual character-sheet. Users can access it either from their own profile or from the list of characters. The document ID-field is used as part of the URL,
# to allow easy external linking for users and to give each document an end-point for the REST-API functionality.


@ app.route("/char-profile/<char_id>", methods=['GET', 'POST'])
def char_profile(char_id):
    character = Char.objects(pk=char_id).first()
    if request.method == 'POST':
        # A very simplistic REST API to pass the character statistics to JavaScript, which will use it to populate fields and features like dice-rolls.
        return jsonify(character.content)
    return render_template('char_profile.html', character=character)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
