import os
from form import AddDogForm
from form import RegisterForm
from flask import Flask, render_template, request, redirect, flash, url_for, session, logging, request, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, FileField, SelectField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from logging.config import dictConfig
from functools import wraps
import uuid
from werkzeug.utils import secure_filename

UPLOADED_IMAGES_DEST = 'uploads/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'leyndo123456'

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

# ------------- connection to the database------------- #

app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'b5aef45b6c5463'
app.config['MYSQL_PASSWORD'] = '6bd17e5d'
app.config['MYSQL_DB'] = 'heroku_5ac0bb6b985dc58'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# ------------- Decorators functions ------------- #


# Check the api key and if it is in the database
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        app.logger.info(request.form)
        if "api_key" not in request.form:
            return jsonify({'message': 'Api key is missing!'}), 403

        api_key = request.form['api_key']

        # # Create Cursor
        cur = mysql.connection.cursor()
        # Check if there is a user with the api key from usr table
        results = cur.execute('SELECT * FROM usr WHERE api_key = %s',
                              [api_key])

        if results > 0:
            usr = cur.fetchone()
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Api key does not exist"}), 403

    return decorated


# Decorator for when logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        else:
            flash('Please log in to access this site', 'danger')
            return redirect(url_for('login'))

    return wrap


# ------------- Functions ------------- #


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# The next 4 functions, GET ALL, ADD, EDIT and DELETE a.k.a (CRUD) are passed in the API and interface routes below in the code


# Function to GET ALL dogs from the database
def get_all_dogs():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get dogs
    result = cur.execute("SELECT * FROM dogs")
    dogs = cur.fetchall()
    # Close connection
    cur.close()
    return dogs


# Function to GET ONE dog from the database
def get_one_dog(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get dogs
    result = cur.execute("SELECT * FROM dogs WHERE id =  %s", [id])
    one_dog = cur.fetchone()
    # Close connection
    cur.close()
    return one_dog


# Function to ADD dog from the database
def add_one_dog():
    form = AddDogForm(request.form)
    app.logger.info(form.validate())
    app.logger.info(request.method)
    if not form.validate():
        app.logger.info(form.errors.items)
        return False
    if request.method == 'POST' and form.validate():
        dogName = form.dogName.data
        dogAge = form.dogAge.data
        owner = form.owner.data
        home = form.home.data
        lastSeen = form.lastSeen.data
        comments = form.comments.data
        area = form.area.data
        # Create cursor
        cur = mysql.connection.cursor()

        # Get dogs
        cur.execute(
            'INSERT INTO dogs(dogName, dogAge, owner, home, lastSeen, comments, area) VALUES(%s,%s,%s,%s,%s,%s,%s)',
            (dogName, dogAge, owner, home, lastSeen, comments, area))

        cur.execute("SELECT * FROM dogs ORDER BY id DESC LIMIT 0, 1")
        add_dog = cur.fetchone()
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        return add_dog


# Function to EDIT one dog from the database
def edit_one_dog(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get dog by id
    result = cur.execute("SELECT * FROM dogs WHERE id = %s", [id])
    edit_dog = cur.fetchone()
    app.logger.info(edit_dog)
    # Get form from class above in the code
    form = AddDogForm(request.form)
    # Populate dog form fields
    form.dogName.data = dog['dogName']
    form.dogAge.data = dog['dogAge']
    form.owner.data = dog['owner']
    form.home.data = dog['home']
    form.lastSeen.data = dog['lastSeen']
    form.comments.data = dog['comments']

    if request.method == 'POST' and form.validate():
        dogName = request.form['dogName']
        dogAge = request.form['dogAge']
        owner = request.form['owner']
        home = request.form['home']
        lastSeen = request.form['lastSeen']
        comments = request.form['comments']
        # # Create Cursor
        cur = mysql.connection.cursor()
        # # Execute
        cur.execute(
            "UPDATE dogs SET dogName=%s, dogAge=%s, owner=%s, home=%s, lastSeen=%s, comments=%s WHERE id = %s",
            (dogName, dogAge, owner, home, lastSeen, comments, id))

        # # Commit to DB
        mysql.connection.commit()
        # # Close connection
        cur.close()

    return edit_dog()


# Function to DELETE one dog from the database
def delete_one_dog(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get dogs
    result = cur.execute("DELETE FROM dogs WHERE id =  %s", [id])
    delete_dog = cur.fetchone()
    # commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    return delete_dog


# ------------- API routes CRUD ------------- #


# API for ALL dogs
@app.route("/api/all", methods=["GET", "POST"])
@api_key_required
def json_all():
    # dogs is coming from the function
    dogs = get_all_dogs()
    return jsonify(dogs)


# API to GET ONE dog
@app.route("/api/dog/<string:id>/", methods=["GET"])
@api_key_required
def json_one_dog(id):
    # one_dog is coming from the function
    one_dog = get_one_dog(id)
    return jsonify(one_dog)


# API to ADD ONE dog
@app.route("/api/dog/add/", methods=["POST"])
@api_key_required
def json_add_dog():
    # one_dog is coming from the function
    added_dog = add_one_dog()
    if not added_dog:
        return "error", 500
    msg = "Dog has been added"
    return jsonify(added_dog, msg)


# API to get EDIT one dog
@app.route("/api/dog/edit/<string:id>/", methods=["PUT", "POST"])
@api_key_required
def json_edit_dog(id):
    # edit_dog is coming from the function
    edit_dog = edit_one_dog(id)
    return jsonify(edit_dog)


# API to get DELETE one dog
@app.route("/api/dog/delete/<string:id>/", methods=["DELETE"])
@api_key_required
def json_delete_dog(id):
    # delete_dog is coming from the decorator
    delete_dog = delete_one_dog(id)
    # Message that will show if it was success
    msg = "Dog has been deleted"
    return jsonify(delete_dog, msg)


# ------------- Routes for the interface ------------- #


# Route to mainpage / show all dogs
@app.route("/")
def home():
    # get_all_dog is a function further up in the code
    dogs = get_all_dogs()
    if dogs:
        return render_template("index.html", dogs=dogs)
    else:
        msg = "There are no dog missing"
        return render_template("index.html", msg=msg)
    # Close connection
    cur.close()


# Dogs --showing all dogs that have been added missing
@app.route('/dogs', methods=["GET", "POST"])
def dogs():
    # get_all_dog is a function further up in the code
    dogs = get_all_dogs()
    if dogs:
        return render_template("dogs.html", dogs=dogs)
    else:
        msg = "There are no dog missing"
        return render_template("dogs.html", msg=msg)


# To display one dog
@app.route("/dog/<string:id>/")
def dog(id):
    # get_one_dog is a function further up in the code
    dog = get_one_dog(id)
    return render_template("dog.html", dog=dog)


# Add missing dog form --the data will go to MySql
@app.route('/add-dog', methods=['GET', 'POST'])
@is_logged_in
def add_dog():
    form = AddDogForm(request.form)
    if request.method == 'POST' and form.validate():
        dogName = form.dogName.data
        dogAge = form.dogAge.data
        owner = session['user']['id']
        home = form.home.data
        lastSeen = form.lastSeen.data
        comments = form.comments.data
        area = form.area.data
        image = form.image.data
        file = request.files['file']
        filename = secure_filename(file.filename)

        # # Create Cursor
        cur = mysql.connection.cursor()
        # # Execute
        cur.execute(
            'INSERT INTO dogs(dogName, dogAge, owner, home, lastSeen, comments, area, image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
            (dogName, dogAge, owner, home, lastSeen, comments, area, image))
        # # Commit to DB
        mysql.connection.commit()
        # # Close connection
        cur.close()
        flash('Missing dog added', "success")
        return redirect(url_for('dashboard'))
    return render_template('add-dog.html', form=form)


# Edit missing dog form
@app.route('/edit-dog/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_doggy(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get dog by id
    result = cur.execute("SELECT * FROM dogs WHERE id = %s", [id])
    dog = cur.fetchone()
    app.logger.info(dog)
    # Get form
    form = AddDogForm(request.form)
    # Populate dog form fields
    form.dogName.data = dog['dogName']
    form.dogAge.data = dog['dogAge']
    form.home.data = dog['home']
    form.lastSeen.data = dog['lastSeen']
    form.comments.data = dog['comments']

    if request.method == 'POST' and form.validate():
        dogName = request.form['dogName']
        dogAge = request.form['dogAge']
        home = request.form['home']
        lastSeen = request.form['lastSeen']
        comments = request.form['comments']
        # # Create Cursor
        cur = mysql.connection.cursor()
        # # Execute
        cur.execute(
            "UPDATE dogs SET dogName=%s, dogAge=%s, home=%s, lastSeen=%s, comments=%s WHERE id = %s",
            (dogName, dogAge, home, lastSeen, comments, id))
        # # Commit to DB
        mysql.connection.commit()
        # # Close connection
        cur.close()
        flash('Information has been updated', "success")
        return redirect(url_for('dashboard'))
    return render_template('edit-dog.html', form=form)


# Delete missing dog
@app.route("/delete-dog/<string:id>", methods=["POST"])
@is_logged_in
def delete_dog(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM dogs WHERE id = %s", [id])
    # commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    return redirect(url_for('dashboard'))


# Rendering the dashboard template
@app.route('/dashboard')
@is_logged_in
def dashboard():

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM dogs WHERE owner = %s",
                         [session['user']['id']])
    dogs = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', dogs=dogs)

    else:
        msg = 'Not dogs found :('
        return render_template('dashboard.html', msg=msg)

    cur.close()


# Rendering the dashboard template
@app.route('/api-docs')
@is_logged_in
def api_docs():
    return render_template('api-docs.html')


# signup form
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        api_key = uuid.uuid1()

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usr(name, email, username, password, api_key) VALUES(%s, %s, %s, %s, %s)",
            (name, email, username, password, api_key))

        mysql.connection.commit()
        cur.close()
        flash('Signup succesful!', "success")

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


# login form
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password_submitted = request.form['password']

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM usr WHERE username = %s",
                             [username])

        if result > 0:
            user = cur.fetchone()
            password = user['password']

            if sha256_crypt.verify(password_submitted, password):
                session['logged_in'] = True
                session['username'] = username
                session['api_key'] = user["api_key"]
                session['user'] = user

                flash('You are now logged in', 'success')
                return redirect(url_for('add_dog'))
            else:
                error = 'Password and user do not match'
                return render_template('login.html', error=error)

        else:
            error = 'No user found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# log out
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out, doggy', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()