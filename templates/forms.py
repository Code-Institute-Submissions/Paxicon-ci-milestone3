# This file contains Flask-WTF form classes.

from flask-wtf import wtf, FlaskForm


# Registration form, can also be passed without issue to login-page.

class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=20)])
    submit = SubmitField("Submit")
