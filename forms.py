# This file contains Flask-WTF form classes.

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, ValidationError
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired


# Registration form, can also be passed without issue to login-page.

class RegForm(FlaskForm):
    display_name = StringField()
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8)])
    submit = SubmitField("Confirm account-deletion")

# Form for requesting password-reset email


class LostPass(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    submit = SubmitField("Submit password request")
