from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms import DecimalField,EmailField,PasswordField
from wtforms.validators import DataRequired,EqualTo
from flask import render_template
from flask_bootstrap import Bootstrap

app =Flask("HI")


app.config['SECRET_KEY'] = "hello_everynyan"



class SignupForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    prn = DecimalField("Prn",validators=[DataRequired()])
    mail = EmailField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),EqualTo(fieldname='confirm',message="password must match")])
    confirm = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    prn = DecimalField("Prn",validators=[DataRequired()])
    password =PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/signup',methods=['GET','POST'])
def signup():
    name = None
    prn = None
    mail = None
    password= None
    confirm =None
    form = SignupForm()
    if form.validate_on_submit():
        name =form.name.data
        prn = form.prn.data
        mail = form.mail.data
        password =form.password.data
        confirm = form.confirm.data
        
        # DATABASE
    return render_template('signup.html',name=name,prn=prn,mail=mail,form =form)
@app.route('/login',methods=['GET','POST'])
def login():
    name = None
    prn = None
    password =None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        prn = form.name.data
        password = form.password.data

        # DATABASE 
    return render_template("login.html",name=name,prn=prn,form=form)
    



app.run(debug=True)
