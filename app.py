from flask import Flask, render_template, request, redirect


app = Flask(__name__)


# route to mainpage
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
