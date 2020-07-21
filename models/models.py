# flask db init - it means we are initializing the database
# flask db migrate - migrating our model to our database
# flask db upgrade - finalizing the migration between model and database

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

  posts = db.relationship('Posts', backref="editor_posts", cascade="all, delete-orphan", lazy=True)
  reviews = db.relationship('Reviews', cascade="all, delete-orphan", backref="editor_reviews", lazy=True)
  liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', cascade="all, delete-orphan", backref='user', lazy='dynamic')

  
  def like_post(self, post):
    if not self.has_liked_post(post):
      like = PostLike(user_id=self.id, item_id=post.id)
      db.session.add(like)

  def unlike_post(self, post):
    if self.has_liked_post(post):
      PostLike.query.filter_by(
          user_id=self.id,
          item_id=post.id).delete()

  def has_liked_post(self, post):
    return PostLike.query.filter(
      PostLike.user_id == self.id,
      PostLike.item_id == post.id).count() > 0

class Categories(db.Model):

  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  image = db.Column(db.String(100), nullable=False)

  create_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
  update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  posts = db.relationship('Posts', backref="categories", cascade="all, delete-orphan", lazy=True)

class Posts(db.Model):

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
  name = db.Column(db.String(30), nullable=False)
  content = db.Column(db.String(280), nullable=False)
  image = db.Column(db.String(100), nullable=True)

  create_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
  update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

  # reviews = db.relationship('Reviews', backref="author", cascade="all, delete-orphan", lazy=True)
  reviews = db.relationship('Reviews', backref="author", cascade="all, delete-orphan", lazy=True, order_by='Reviews.update_at.desc()')
  likes = db.relationship('PostLike', backref='posts', cascade="all, delete-orphan", lazy='dynamic')

  def average(self):
    count = 0
    for i in self.reviews:
      count = count + i.score
    try:
      average = round(count / len(self.reviews), 1)
    except ZeroDivisionError:
      average = 0 
    return average

class Reviews(db.Model):

  __tablename__ = 'reviews'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  item_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
  title = db.Column(db.String(30), nullable=False)
  content = db.Column(db.String(280), nullable=False)
  score = db.Column(db.Float, nullable=False)

  create_at = db.Column(db.DateTime, nullable=False, default=datetime.now) 
  update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class PostLike(db.Model):

  __tablename__ = 'post_likes'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  item_id = db.Column(db.Integer, db.ForeignKey('posts.id'))