from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
