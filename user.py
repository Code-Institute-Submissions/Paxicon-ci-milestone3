from app import db
import flask_mongoengine
from flask_login import UserMixin


class User(UserMixin, db.Document):
    email = db.StringField(required=True)
    password = db.PasswordField(required=True)