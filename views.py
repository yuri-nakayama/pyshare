# docker-compose build
# docker-compose up
# docker container ls -a
# docker exec -i -t container_name /bin/bash

# contains our functions to connect HTML and Python¥
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify      # importing necssary flask modules
from .app import app                  # connection to app.py
from .database import db              # connection to db
from passlib.hash import sha256_crypt # encryping the password - to change random strings
# pip3 install passlib
from .models.models import User, Categories, Posts, Reviews, PostLike       # importing the models - to access the models
from flask_login import login_user, LoginManager, login_required, current_user, logout_user   # this is for our login session and we will use the flask_login module
# from datetime import datetime
    
login_manager = LoginManager() # creating an object of class LoginManager()
login_manager.init_app(app) # passing the parameter and initialize app inseide the login_manager

# Index
@app.route("/")
def index():
  return render_template("index.html") # URL and to pass the data

# About
@app.route("/about")
def about():
  return render_template("about.html") # URL and to pass the data

# User Register
@app.route("/register", methods=["GET", "POST"])
def register():

  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    user = User(name=username, password=sha256_crypt.encrypt(password)) # encryption
    db.session.add(user)  # inserting to the table
    db.session.commit()   # commit

    flash('You are now registered and can log in', 'success')
    return render_template("login.html") # URL and to pass the data

  return render_template("register.html") # URL and to pass the data

# Login
@app.route("/login", methods=["GET", "POST"])
def login():

  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(name=username).first()
    if user is not None and user.name == username:
      validate = sha256_crypt.verify(password, user.password) # comparing the input data and the database data
      if validate == True:
        login_user(user)  # Flask
        flash('You are now logged in','success')
        return redirect(url_for('dashboard', id=user.id)) # to go to route directly and it is allowed to put only one argument

      else:
        flash('Invalid Password Provided','danger') # 
        return render_template("login.html")
  
    else:
      flash('User is not found','danger')
      flash('Username is incorrect!','danger')
      return render_template("login.html")

  return render_template("login.html")

# Logout
@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You are now logged out','success')
  return render_template("login.html")

@login_manager.user_loader # checking the user and its id, so that it can access the /timeline
def load_user(id):         # this means checking the id of the user that can access the /timeline
  return User.query.get(int(id)) # flask wants to know the current data

# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
  # posts = Posts.query.filter_by().all()
  posts = Posts.query.filter_by(user_id=current_user.id).order_by(Posts.update_at.desc()).all()
  for post in posts:
    post.likes.count()
    post.average()

  categories = Categories.query.filter_by().all()

  return render_template("dashboard.html", posts=posts, categories=categories) # URL and to pass the data

''' User '''
# Profile
@app.route("/profile/<int:id>")
@login_required
def profile(id):

  user = User.query.filter_by(id=id).first()

  return render_template("profile.html", user=user)

# Update User
# @app.route("/user/update/<int:id>", methods=["GET", "POST"])
@app.route("/profile/update/<int:id>", methods=["GET", "POST"])
@login_required
def upd_user(id):

  if request.method == "POST":
    # checking if the data is existed
    user = User.query.filter_by(id=id).first()
    user.name = request.form["username"]
    user.email = request.form["email"]
    user.bio = request.form["bio"]
    db.session.commit()  # commit/persists/finalize those changes to the database
    
  flash('You are successful to update','success')
  return redirect(url_for('profile', id=id))  # to go to route

# Update User Image
@app.route("/profile/image/update/<int:id>", methods=["GET", "POST"])
@login_required
def upd_user_image(id):

  if request.method == "POST":
    files = request.files["img"]
    filename = files.filename
    files.save("static/" + filename)
    
    user = User.query.filter_by(id=id).first()
   
    user.profile = filename
    db.session.commit()  # commit/persists/finalize those changes to the database
    
  flash('You are successful to update','success')
  return redirect(url_for('profile', id=id))  # to go to route

# Select User for delete
@app.route("/profile/delete/<int:id>")
@login_required
def disp_user_delete(id):

  user = User.query.filter_by(id=id).first()

  return render_template("del_user.html", user=user)

# Delete User
@app.route("/user/delete/<int:id>", methods=["GET", "POST"])
@login_required
def del_user(id):

  if request.method == "POST":

    # checking if the data is existed
    user = User.query.filter_by(id=id).first()
    password = request.form["password"]

    validate = sha256_crypt.verify(password, user.password)
    if validate == False:
      flash('Invalid Password Provided', 'danger')
      return render_template("del_user.html", user=user)

    db.session.delete(user)
    db.session.commit()   # commit/persists/finalize those changes to the database

  logout_user()
  flash('Thank you so much!', 'success')
  return render_template("login.html")

''' Post '''
# Post
@app.route("/item/<int:id>")
def post(id):
  post = Posts.query.filter_by(id=id).first() 
  post.likes.count()
  post.average()

  return render_template("post.html", post=post) # URL and to pass the data

# Add Post
@app.route("/post/add", methods=['GET', 'POST'])
@login_required
def add_post():

  if request.method == "POST":
    files = request.files["image"]
    filename = files.filename

    files.save("static/" + filename)
    
    user_id = current_user.id
    category = request.form["category"]
    name = request.form["name"]
    content = request.form["content"]
    image = filename

    post = Posts(user_id=user_id, category_id=category, name=name, content=content, image=image) # encryption
    db.session.add(post)  # inserting to the table
    db.session.commit()   # commit

    flash('You are successful to add','success')
    return redirect(url_for('dashboard', id=user_id))

  else:
    categories = Categories.query.filter().all()

  return render_template("add_post.html", categories=categories)

# Update Post
@app.route("/post/update/<int:id>", methods=["GET", "POST"])
@login_required
def upd_post(id):

  post = Posts.query.filter_by(id=id).first()

  if request.method == "POST":
    files = request.files["image"]
    filename = files.filename

    files.save("static/" + filename)
    
    user_id = current_user.id
    category = request.form["category"]
    name = request.form["name"]
    content = request.form["content"]
    image = filename

    post.name = name
    post.category_id = category
    post.content = content
    post.image = image
    db.session.commit()  # commit/persists/finalize those changes to the database
    
    flash('You are successful to update','success')
    return redirect(url_for('dashboard', id=user_id))

  else:
    categories = Categories.query.filter().all()
    
  return render_template("upd_post.html", post=post, categories=categories)

# Delete Post
@app.route("/post/delete/<int:id>")
def del_post(id):
  post = Posts.query.filter_by(id=id).first()
  db.session.delete(post)

  db.session.commit()   # commit

  flash('You are successful to delete','warning')
  return redirect(url_for('dashboard', id=current_user.id))

''' Review '''
# Review
@app.route("/review/<int:id>")
@login_required
def review(id):
  post = Posts.query.filter_by(id=id).first()
  post.average()

  return render_template("review.html", post=post) # URL and to pass the data

# Add Review
@app.route("/review/add/<int:id>", methods=['GET', 'POST'])
@login_required
def add_review(id):

  if request.method == "POST":
    user_id = current_user.id
    item_id = id
    title = request.form["title"]
    content = request.form["content"]
    score = request.form["radio"]

    review = Reviews(user_id=user_id, item_id=item_id, title=title, content=content, score=score) # encryption
    db.session.add(review)  # inserting to the table
    db.session.commit()   # commit

  flash('You are successful to add','success')
  return redirect(url_for('review', id=item_id))

# Update Review
@app.route("/review/update/<int:id>", methods=["GET", "POST"])
@login_required
def upd_review(id):

  review = Reviews.query.filter_by(id=id).first()

  if request.method == "POST":
    review.title = request.form["title"]
    review.content = request.form["content"]
    review.score = request.form["radio"]
    db.session.commit()  # commit/persists/finalize those
    
    flash('You are successful to update','success')
    return redirect(url_for('review', id=review.item_id))  # to go to route

  return render_template('upd_review.html', review=review)

# Delete Review
@app.route('/review/delete/<int:id>')
@login_required
def del_review(id):

  review = Reviews.query.filter_by(id=id).first()

  db.session.delete(review)
  db.session.commit()

  flash('You are successful to delete','warning')
  return redirect(url_for('review', id=review.item_id))  # to go to route

''' PostLike '''
@app.route('/like/<int:post_id>/<action>')
# @login_required
def like_action(post_id, action):

  post = Posts.query.filter_by(id=post_id).first_or_404()
  
  if action == 'like':
    current_user.like_post(post)
    db.session.commit()

  if action == 'unlike':
    current_user.unlike_post(post)
    db.session.commit()
    
  return redirect(request.referrer)

''' Category '''
# Category
@app.route("/category")
# @login_required
def category():
  categories = Categories.query.filter_by().all()

  return render_template("category.html", categories=categories) # URL and to pass the data

# Add Category
@app.route("/category/add", methods=['GET', 'POST'])
# @login_required
def add_category():

  if request.method == "POST":
    files = request.files["image"]
    filename = files.filename

    files.save("static/" + filename)
    
    name = request.form["name"]
    image = filename

    category = Categories(name=name, image=image) # encryption
    db.session.add(category)  # inserting to the table
    db.session.commit()   # commit

  flash('You are successful to add','success')
  return redirect(url_for('category'))

# Update Category
@app.route("/category/update/<int:id>", methods=['GET', 'POST'])
# @login_required
def upd_category(id):

  category = Categories.query.filter_by(id=id).first()

  if request.method == "POST":
    files = request.files["image"]
    filename = files.filename

    files.save("static/" + filename)
    
    category.name = request.form["name"]
    category.image = filename
    db.session.commit()  # commit/persists/finalize those
    
    flash('You are successful to update','success')
    return redirect(url_for('category'))

  return render_template("upd_category.html", category=category) # URL and to pass the data

# Delete Category
@app.route('/category/delete/<int:id>')
# @login_required
def del_category(id):

  category = Categories.query.filter_by(id=id).first()

  db.session.delete(category)
  db.session.commit()

  flash('You are successful to delete','warning')
  return redirect(url_for('category'))


''' Search '''
# Search
@app.route("/search", methods=['GET', 'POST'])
# @login_required
def search():

  categories = Categories.query.filter_by().all()

  if request.method == "POST":
    wherevalue = []
    
    # category
    category = request.form["category"]
    if not category == "":
      wherevalue.append(Posts.category_id == category)
    
    # search keyword
    search = request.form["search"]
    if not search == "":
      wherevalue.append(Posts.name.like("%{}%".format(search)))
    
    # score
    score = request.form["radio"]
    # it will apply after getting the post data
    
    # favorite
    try:
      favorite = request.form["checkbox"]

      in_claus_val = []
      postlikes = PostLike.query.filter_by(user_id=current_user.id).all()
      if postlikes is not None:
        for postlike in postlikes:
          in_claus_val.append(postlike.item_id)

        wherevalue.append(Posts.id.in_(in_claus_val))
        
      else:
        return render_template("search.html", posts="", categories=categories)  # URL and to pass the data 

    except:
      # when the checkbox isn't checked
      pass    

    if category == "" and category == "" and score == "" and favorite == "":
      flash('Input something...','warning')
      return redirect(request.referrer)

    whereclause = ""
    for where in wherevalue:
      whereclause = where + ", "

    posts = Posts.query.filter(whereclause, Posts.user_id!=current_user.id).order_by(Posts.update_at.desc()).all()
    # for post in posts:
    #   post.average()
    if not score == "":

      tmp_posts = []
      for post in posts:
        # if the numberis grater than or equal to score
        if post.average() >= float(score):
          tmp_posts.append(post)
      posts = tmp_posts

  else:
    posts = Posts.query.filter(Posts.user_id!=current_user.id).order_by(Posts.update_at.desc()).all()
    # for post in posts:
    #   post.average()

  return render_template("search.html", posts=posts, categories=categories)  # URL and to pass the data