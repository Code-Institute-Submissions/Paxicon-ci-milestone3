# This file contains Flask-WTF form classes and validator methods from the following imports.

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, TextAreaField, ValidationError
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired


# Registration form, passed for registration and login functions.

class RegForm(FlaskForm):
    display_name = StringField('Display name: ', [InputRequired(message='You must provide a display name!'), Length(
        min=1, max=20, message="Display name must be between  and 20 characters long!")])
    email = StringField('Email: ',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    password = PasswordField('Password: ', [InputRequired(message='You must provide a password!'), Length(
        min=8, max=20, message="Your password must be between 8 and 20 characters long!")])
    submit = SubmitField("Login")

# Form for requesting password-reset email.


class LostPass(FlaskForm):
    email = StringField('Email: ',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    submit = SubmitField("Submit password request")

# Form for about.html MailMe-modal.


class MailMeForm(FlaskForm):
    email = StringField('Email: ',  validators=[InputRequired(), Email(
        message='Invalid email')])
    subject = StringField('Subject: ', [InputRequired(
        message='You must enter a message subject!')])
    message = TextAreaField('Message: ', [InputRequired(message='You cannot submit an empty message!'), Length(
        min=1, max=500, message="Your message must be between 1 and 500 characters long!")])
    submit = SubmitField("Send email")
