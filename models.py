from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
	username = db.Column(db.String(24), primary_key=True)
	pw_hash = db.Column(db.String(64), nullable=False)
	currently_reading = db.Column(db.String(80), db.ForeignKey('book.title'))

	updates = db.relationship('Update', backref='author')

	follows = db.relationship('User', secondary='follows', # uses the table follows to connect the two users
		primaryjoin='User.username==follows.c.follower_username',
		secondaryjoin='User.username==follows.c.followee_username',
		backref=db.backref('followed_by', lazy='dynamic'), lazy='dynamic')

	def __init__(self, username, pw_hash):
		self.username = username
		self.pw_hash = pw_hash

	def __repr__(self):
		return '<User {}>'.format(self.username)

follows = db.Table('follows',
	db.Column('follower_username', db.Integer, db.ForeignKey('user.username')),
	db.Column('followee_username', db.Integer, db.ForeignKey('user.username'))
)

class Update(db.Model):
	update_id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(32), nullable=False)
	author_username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
	book_title = db.Column(db.String(80), db.ForeignKey('book.title'), nullable=False)
	content = db.Column(db.Text, nullable=True)
	rating = db.Column(db.Integer, nullable=True)
	timestamp = db.Column(db.Integer)

	def __init__(self, type, author_username, book_title, content, rating, timestamp):
			self.type = type
			self.author_username = author_username
			self.book_title = book_title
			self.content = content
			self.rating = rating
			self.timestamp = timestamp

	def __repr__(self):
			return '<Update {}'.format(self.update_id)

class Book(db.Model):
	title = db.Column(db.String(80), primary_key=True)
	author = db.Column(db.String(80), nullable=False)
	image = db.Column(db.String(80), nullable=False)
	rating = db.Column(db.Integer, nullable=True)
	num_ratings = db.Column(db.Integer, nullable=True)

	def __init__(self, title, author, image):
			self.title = title
			self.author = author
			self.image = image

	def __repr__(self):
			return '<Book {}'.format(self.title)
