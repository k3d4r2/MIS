from flask import Flask, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import DecimalField, EmailField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, InputRequired
from flask_bootstrap import Bootstrap
import json
import sys
import pyrebase
import re
import requests


config = None
with open("config.json") as config_file:
    config = json.load(config_file)

if not config:
    print("config file not found")
    sys.exit(1)

app = Flask(__name__, static_folder='./static')

app.config['SECRET_KEY'] = "hello_everynyan"

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


def httpErrortoJSON(http_error):
    http_error = json.loads(re.sub(r'\[.*?\]', '', str(http_error)))
    return http_error


class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    prn = IntegerField("PRN", validators=[DataRequired()])
    mail = EmailField("Email",  validators=[DataRequired()])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo(fieldname='confirm',
                                                     message="Oops! It seems like the passwords you entered don't match. Please check and try again.")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    prn = DecimalField("PRN", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        prn = form.prn.data
        mail = form.mail.data
        password = form.password.data
        confirm = form.confirm.data

        try:
            auth.create_user_with_email_and_password(mail, password)
            flash('Created successfull ' + name)
        except requests.exceptions.HTTPError as e:
            response = httpErrortoJSON(e)
            if response['error']['code'] == 400:
                flash("Email already exists!")

        return redirect(url_for("login"))

    # passwords don't match
    if (form.password.errors):
        print(form.password.errors)
        flash(form.password.errors[0])

    return render_template("signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    name = None
    prn = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():

        name = form.name.data
        prn = form.name.data
        password = form.password.data

        # DATABASE
    return render_template("login.html", name=name, prn=prn, form=form)


if __name__ == "__main__":
    app.run(debug=True)
