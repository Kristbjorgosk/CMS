from flask import Flask, render_template, request, redirect
from data import Data


app = Flask(__name__)

Data = Data()

# route to mainpage
@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/dogs")
# def articles():
#     return render_template("dogs.html", dogs=dogs)

if __name__ == "__main__":
    app.run(debug=True)