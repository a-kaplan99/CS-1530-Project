from models import db, User, Book, Update
import sqlalchemy
import time
import os
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# configuration
PER_PAGE = 30
DEBUG = True
SECRET_KEY = '123456'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'hillman_social.db')

app.config.from_object(__name__)
app.config.from_envvar('HILLMAN_SOCIAL_SETTINGS', silent=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #here to silence deprecation warning

db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.create_all()
	print('Initialized the database.')

@app.route("/")
def default():
	return redirect(url_for("login"))

@app.route("/login/", methods=["GET", "POST"])
def login():
	error = None
	user = None
	if 'username' in session: # You can't login twice, go to your main page
		return redirect(url_for('timeline'))
	if request.method == "POST":
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		else:
			user = User.query.filter_by(username=request.form['username']).first()
			if user == None:
				error = "Invalid username"
			if user != None:
				error = login(user, request.form["password"])
				if error == None:
					return redirect(url_for('books'))

	return render_template('login.html', error=error)

def login(user, password):
	if not check_password_hash(user.pw_hash, password):
		return "Invalid password"
	session['username'] = user.username
	return None

@app.route("/register/",  methods=["POST", "GET"])
def register():
	error = None
	if request.method == "POST":
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		else:
			user = User(request.form['username'], generate_password_hash(request.form['password']))
			db.session.add(user)
			db.session.commit()
			db.session.flush()

			flash("Welcome " + request.form['username'] + "! ")
			flash("You have successfully registered for an account!")
			session['username'] = user.username # Allows the session to remember user is logged in
	return render_template('register.html', error=error)

@app.route("/logout/",  methods=["GET"])
def logout():
	flash("You have been logged out.")
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route("/books/",  methods=["POST", "GET"])
def books():
	error = None
	if 'username' not in session:
		abort(401) # Not authorized
	# Get the user
	user = User.query.filter_by(username=session['username']).first()
	books = Book.query.order_by(Book.title.asc()).all()
	if not user:
		abort(404)
	return render_template("books.html", error=error, user_name=user.username, books=books)

@app.route("/timeline/",  methods=["POST", "GET"])
def timeline():
	error = None
	if 'username' not in session:
		abort(401) # Not authorized
	# Get the user
	user = User.query.filter_by(username=session['username']).first()
	updates = Update.query.order_by(Update.timestamp.desc()).limit(PER_PAGE).all()
	if not user:
		abort(404)
	return render_template("timeline.html", error=error, user_name=user.username, updates=updates)

@app.route("/review/<book_title>", methods=["POST", "GET"])
def review(book_title):
	if 'username' not in session:
		abort(401)
	error = None
	if request.method == 'POST':
		if not request.form['rating']:
			error = 'Please give this book a rating from 1 - 10'
		else:
			# update rating for book
			book = Book.query.filter_by(title=book_title).first()
			old_rating = book.rating
			if old_rating is None:
				book.rating = request.form['rating']
				book.num_ratings = 1
			else:
				book.rating = round(((old_rating * book.num_ratings) + int(request.form['rating'])) / (book.num_ratings + 1), 1)
				book.num_ratings += 1

			db.session.add(Update('review', session['username'], book_title, request.form['content'], request.form['rating'], time.time()))
			db.session.commit()
			db.session.flush()
			flash("Submission successful")
	return render_template('review.html', book=Book.query.filter_by(title=book_title).first(), error=error)

@app.route("/refresh/")
def refresh():
	if Book.query.filter_by(title='The Catcher in the Rye').first() is None:
		db.session.add(Book('The Catcher in the Rye', 'J.D. Salinger', 'catcher.jpg'))
		db.session.commit()
		db.session.flush()
	return redirect(url_for('books'))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
	db.create_all()
    app.run(threaded=True, port=5000)
