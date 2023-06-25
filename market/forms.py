from wtforms import StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm


class RegistrationField(FlaskForm):
    username = StringField(label="User Name")
    email_address = StringField(label="Email")
    password1 = PasswordField(label="Password")
    password2 = PasswordField(label="Confirm Password")
    submit = SubmitField(label="Create Account")