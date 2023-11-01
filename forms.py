
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import DecimalField, EmailField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, InputRequired


class SignupForm(FlaskForm):
    # name = StringField("Name", validators=[DataRequired()])
    # prn = IntegerField("PRN", validators=[DataRequired()])
    mail = EmailField("Email",  validators=[DataRequired()])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo(fieldname='confirm',
                                                     message="Oops! It seems like the passwords you entered don't match. Please check and try again.")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    mail = EmailField("Email", validators=[DataRequired()])
    # prn = DecimalField("PRN", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
