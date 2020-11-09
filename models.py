from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False)
	pw_hash = db.Column(db.String(64), nullable=False)

	updates = db.relationship('Update', backref='author')

	reading = db.relationship('Book', secondary='reading', # uses the table follows to connect the two users
		primaryjoin='User.user_id==reading.c.reader_id',
		secondaryjoin='Book.book_id==reading.c.book_id',
		backref=db.backref('read_by', lazy='dynamic'), lazy='dynamic')

	follows = db.relationship('User', secondary='follows', # uses the table follows to connect the two users
		primaryjoin='User.user_id==follows.c.follower_id',
		secondaryjoin='User.user_id==follows.c.followee_id',
		backref=db.backref('followed_by', lazy='dynamic'), lazy='dynamic')

	def __init__(self, username, pw_hash):
		self.username = username
		self.pw_hash = pw_hash

	def __repr__(self):
		return '<User {}>'.format(self.username)

follows = db.Table('follows',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.user_id')),
	db.Column('followee_id', db.Integer, db.ForeignKey('user.user_id'))
)

reading = db.Table('reading',
	db.Column('reader_id', db.Integer, db.ForeignKey('user.user_id')),
	db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'))
)

class Update(db.Model):
	update_id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
	text = db.Column(db.Text, nullable=False)
	pub_date = db.Column(db.Integer)

	def __init__(self, author_id, text, pub_date):
			self.author_id = author_id
			self.text = text
			self.pub_date = pub_date

	def __repr__(self):
			return '<Update {}'.format(self.update_id)

class Book(db.Model):
	book_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	author = db.Column(db.String(80), nullable=False)
	image = db.Column(db.String(80), nullable=False)

	def __init__(self, title, author, image):
			self.title = title
			self.author = author
			self.image = image

	def __repr__(self):
			return '<Book {}'.format(self.book_id)
