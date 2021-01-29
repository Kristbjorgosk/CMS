from flask import Flask, render_template, request, redirect, flash, url_for, session, logging, request
from data import Data
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
#from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'leyndo123456'

app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'b5aef45b6c5463'
app.config['MYSQL_PASSWORD'] = '6bd17e5d'
app.config['MYSQL_DB'] = 'heroku_5ac0bb6b985dc58'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

'''
# connecting database sqlite to the folder newbooking.db thats stores all the data that is inputed
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogs.db'
db = SQLAlchemy(app)


# database model
class Dogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(200))
    email = db.Column(db.String(200))
    dogName = db.Column(db.String(200))
    dogAge = db.Column(db.String(200))
    home = db.Column(db.String(200))
    lastSeen = db.Column(db.String(200))
    comments = db.Column(db.Text())
   

    def __init__(self, owner, email, dogName, dogAge, home, lastseen, comments):
        self.owner = owner
        self.email = email
        self.dogName = dogName
        self.dogAge = dogAge
        self.home = home
        self.lastSeen = lastSeen
        self.comments = comments
 '''

# route to mainpage


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login-register", methods=["GET", "POST"])
def loginRegister():
    return render_template("login-register.html")


@app.route("/submit-missing", methods=["GET", "POST"])
def submitMissing():
    return render_template("submit-missing.html")


@app.route("/all-dogs", methods=["GET", "POST"])
def allDogs():
    dogs = Dogs.query.all()
    return render_template("all-dogs.html")

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
    validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usr(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        mysql.connection.commit()

        cur.close()

        flash('Signup succesful!')

        redirect(url_for ('signup'))
    return render_template('signup.html', form=form)

# @app.route("/dogs")
# def articles():
#     return render_template("dogs.html", dogs=dogs)

if __name__ == "__main__":
    app.run(debug=True)
