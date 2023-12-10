from flask import Flask, render_template, flash, url_for, redirect, session
import json
import sys
import pyrebase
import re
import requests
from forms import SignupForm, LoginForm
from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth


config = None

with open("config.json") as config_file:
    config = json.load(config_file)

if not config:
    print("config file not found")
    sys.exit(1)

app = Flask(__name__, static_folder='./static')

app.config['SECRET_KEY'] = "hello_everynyan"
app.config['SESSION_TYPE'] = 'filesystem'


cred = credentials.Certificate("./mis-dummy.json")
firebase_admin.initialize_app(cred)


firebase = pyrebase.initialize_app(config)
client_auth = firebase.auth()

# session.permanent = False


def httpErrortoJSON(http_error):
    http_error = json.loads(re.sub(r'\[.*?\]', '', str(http_error)))
    return http_error


def login_required(func):
    wraps(func)

    def secure_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return secure_function


def admin_required(func):
    wraps(func)

    def secure_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return secure_function


def is_admin(uid):
    '''
        Generic method which return True if user is admin or else false
    '''
    user = auth.get_user(uid)
    if user.custom_claims is not None:
        if 'admin' in user.custom_claims:
            return True
    return False


@app.route('/make-admin/<uid>')
def make_admin(uid):
    auth.set_custom_user_claims(uid, {'admin': True})
    return {"response": "Made admin"}


@app.route('/remove-admin/<uid>')
def remove_admin(uid):
    auth.set_custom_user_claims(uid, {'admin': False})
    return {"response": "Removed admin"}


@app.route("/get-user/<uid>")
def get_user(uid):
    user_record = auth.get_user(uid)
    user_dict = {
        'uid': user_record.uid,
        'email': user_record.email,
    }
    return user_dict


@login_required
@app.context_processor
def is_cur_user_admin():
    '''
    Wrapper function to check if the user is admin or not
    '''
    user = session.get('user')

    if user:
        # uid = user['localId']
        id_token = user['idToken']

        # check if user is admin
        claims = auth.verify_id_token(id_token)

        if 'admin' in claims:
            if claims['admin'] is True:
                return {'is_admin': True}

        return {'is_admin': False}

    return {'is_admin': False}


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if session.get('logged_in'):
        return redirect(url_for("home"))

    form = SignupForm()
    if form.validate_on_submit():
        mail = form.mail.data
        password = form.password.data
        confirm = form.confirm.data

        try:
            user = client_auth.create_user_with_email_and_password(mail, password)
            flash('============Created successfull==============')
            auth.set_custom_user_claims(user["localId"], {'admin': False})
        except requests.exceptions.HTTPError as e:
            response = httpErrortoJSON(e)
            if response['error']['code'] == 400:

                if response['error']['code'] == 'EMAIL_EXISTS':
                    flash("Email already exists")
                    return redirect(url_for('login'))

                flash(response['error']['message'])

                return redirect(url_for('signup'))

        return redirect(url_for("login"))

    # passwords don't match
    if (form.password.errors):
        flash(form.password.errors[0])

    return render_template("signup.html", form=form)


@app.route('/', methods=['GET', 'POST'])
def login():

    if session.get('logged_in'):
        return redirect(url_for("home"))

    password = None
    form = LoginForm()
    if form.validate_on_submit():

        mail = form.mail.data
        password = form.password.data

        # check if user exists
        try:
            user = auth.get_user_by_email(mail)
        except auth.UserNotFoundError:
            flash("User doesn't exists! Please create an account")
            return redirect(url_for('signup'))

        try:
            user = client_auth.sign_in_with_email_and_password(mail, password)
        except requests.exceptions.HTTPError as e:
            response = httpErrortoJSON(e)
            if response['error']['code'] == 400:
                flash("Invalid credentials")
            return redirect(url_for('login'))

        session['user'] = user
        session['logged_in'] = True

        return render_template("home.html")

    return render_template("login.html", form=form)


@app.route('/home', endpoint='home')
@login_required
def home():
    return render_template("home.html")


@app.route('/logout', endpoint='logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for("login"))


@app.route('/users', endpoint='users')
@login_required
def users():
    '''
        route to users page
    '''
    return render_template("users.html")


@app.route('/users-list')
@login_required
def get_users_list():
    page = auth.list_users()

    users = []
    while page:
        for user in page.users:
            users.append({"uid": user.uid, "email": user.email,
                          "admin": user.custom_claims["admin"]})
        page = page.get_next_page()

    return render_template("users-list.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)
