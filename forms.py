# This file contains Flask-WTF form classes.

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, ValidationError
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired


# Registration form, can also be passed without issue to login-page.

class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8)])
    submit = SubmitField("Submit")

# Form for requesting password-reset email


class LostPass(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    submit = SubmitField("Submit password request")

# Form for confirming new password


class ConfirmNewPassForm(FlaskForm):

    password = PasswordField('password', validators=[
                             DataRequired(), Length(min=8, max=20)])
    submit = SubmitField("Change my password!")
