# This file contains setup of the User class for the flask-login extension.
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mongoengine import MongoEngine, Document
from flask_login import UserMixin
import jwt

db = MongoEngine()

# While UserMixin does allow us to inherit the required class attributes, I decided to implement them for clarity of code.

# Since user is classed as a Document, it adheres more rigidly to the schema than other document-models in the project.


class User(UserMixin, db.Document):
    meta = {'collection': 'User'}
    display_name = db.StringField(max_length=50)
    email = db.StringField(max_length=50)
    password = db.StringField()
    # A required attribute from flask-login to ensure the login.required decorators operate functionally. As auth here is very simple, all users are considered authenticated if they pass login.
    is_authenticated = True
    # As required by flask-login. For our purposes, all users are active users.
    is_active = True
    # As required by flask-login. For our purposes, there are no anonymous users.
    is_anonymous = False
    # Method for returning a hashed, secure password.

    def set_pw(self, password):
        return set_pw

    # Method for validating the password of a user.
    def check_pw(self, password):
        return check_password_hash(self['password'], password)
