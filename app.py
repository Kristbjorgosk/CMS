from flask import Flask, render_template, request, redirect, flash, url_for, session, logging, request
from data import Data
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.secret_key = 'leyndo123456'

app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'b5aef45b6c5463'
app.config['MYSQL_PASSWORD'] = '6bd17e5d'
app.config['MYSQL_DB'] = 'heroku_5ac0bb6b985dc58'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# route to mainpage
@app.route("/")
def home():
    return render_template("index.html")


# Dogs --showing all dogs that have been added missing
@app.route('/dogs', methods=["GET", "POST"])
def dogs():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get dogs
    result = cur.execute("SELECT * FROM dogs")
    dogs = cur.fetchall()
    if result > 0:
        return render_template("dogs.html", dogs=dogs)
    else:
        msg = "There are no dog missing"
        return render_template("dogs.html", msg=msg)
    # Close connection
    cur.close()


# Class for missing dog form
class AddDogFrom(Form):
    dogName = StringField('The dog Name', [validators.Length(min=1, max=200)])
    dogAge = StringField('The dogs age', [validators.Length(min=1, max=200)])
    owner = StringField('Name of the owner',
                        [validators.Length(min=1, max=200)])
    home = StringField('Streetname of the dogs home',
                       [validators.Length(min=1, max=200)])
    lastSeen = StringField('Where was he last seen',
                           [validators.Length(min=1, max=200)])
    comments = StringField('Any additional comments?',
                           [validators.Length(min=1, max=1000)])


# Add missing dog form --the data will go to MySql
@app.route('/add-dog', methods=['GET', 'POST'])
def add_dog():
    form = AddDogFrom(request.form)
    if request.method == 'POST' and form.validate():
        dogName = form.dogName.data
        dogAge = form.dogAge.data
        owner = form.owner.data
        home = form.home.data
        lastSeen = form.lastSeen.data
        comments = form.comments.data
        # # Create Cursor
        cur = mysql.connection.cursor()
        # # Execute
        cur.execute(
            'INSERT INTO dogs(dogName, dogAge, owner, home, lastSeen, comments) VALUES(%s,%s,%s,%s,%s,%s)',
            (dogName, dogAge, owner, home, lastSeen, comments))
        # # Commit to DB
        mysql.connection.commit()
        # # Close connection
        cur.close()
        flash('Missing dog added')
        redirect(url_for('add_dog'))
    return render_template('add-dog.html', form=form)


# To display one dog
@app.route("/dog/<string:id>/")
def dog(id):
    # # Create Cursor
    cur = mysql.connection.cursor()
    # Get one dog
    results = cur.execute("SELECT * FROM dogs WHERE id = %s", [id])
    dog = cur.fetchone()
    return render_template("dog.html", dog=dog)


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
        cur.execute(
            "INSERT INTO usr(name, email, username, password) VALUES(%s, %s, %s, %s)",
            (name, email, username, password))

        mysql.connection.commit()

        cur.close()

        flash('Signup succesful!')

        redirect(url_for('signup'))
    return render_template('signup.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
