from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

app = Flask(__name__)
app.secret_key = "ddfdfhdjfhdjh"


class UserForm(FlaskForm):
    name = StringField('Name')
    password = PasswordField('Password')
    submit = SubmitField("Submit")

@app.route('/', methods=["POST", "GET"])
def index():
    form = UserForm()
    if form.validate_on_submit():
        return redirect("/login")
    return render_template("login.html", form=form)

@app.route('/login')
def login_successful():
    return "login"

if __name__ == "__main__":
    app.debug = True
    app.run()
