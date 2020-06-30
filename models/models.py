# inherting db, creating the database table, creating modes
from flaskbasic.database import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin): # this UserMixin is for our login to keep the session data

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  password = db.Column(db.String(100), nullable=False)
  email =  db.Column(db.String(200), nullable=True)
  bio =  db.Column(db.String(280), nullable=True)
  profile = db.Column(db.String(100), nullable=True)
  
  create_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
  update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  posts = db.relationship(('Posts'), backref="editor_posts", lazy=True)
  reviews = db.relationship(('Reviews'), backref="editor_reviews", lazy=True)

class Posts(db.Model):

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  name = db.Column(db.String(30), nullable=False)
  content = db.Column(db.String(280), nullable=False)
  image = db.Column(db.String(100), nullable=True)

  create_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
  update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  reviews = db.relationship(('Reviews'), backref="author", lazy=True)


class Reviews(db.Model):

  __tablename__ = 'reviews'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  item_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
  title = db.Column(db.String(30), nullable=False)
  content = db.Column(db.String(280), nullable=False)
  score = db.Column(db.String(280), nullable=False)

  create_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
  update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)