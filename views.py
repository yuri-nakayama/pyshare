# docker-compose build
# docker-compose up
# docker container ls -a
# docker exec -i -t container_name /bin/bash

# contains our functions to connect HTML and Python¥
import json
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify      # importing necssary flask modules
from .app import app                  # connection to app.py
from .database import db              # connection to db
from passlib.hash import sha256_crypt # encryping the password - to change random strings
# pip3 install passlib
from .models.models import User, Posts, Reviews       # importing the models - to access the models
from flask_login import login_user, LoginManager, login_required, current_user, logout_user   # this is for our login session and we will use the flask_login module

login_manager = LoginManager() # creating an object of class LoginManager()
login_manager.init_app(app) # passing the parameter and initialize app inseide the login_manager

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    user = User(name=username, password=sha256_crypt.encrypt(password)) # encryption
    db.session.add(user)  # inserting to the table
    db.session.commit()   # commit

    return redirect("/") # just URL

  return render_template("register.html") # URL and to pass the data

@app.route("/login", methods=["GET", "POST"])
def login():

  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(name=username).first()
    if user is not None and user.name == username:
      validate = sha256_crypt.verify(password, user.password) # comparing the input data and the database data
      if validate == True:
        login_user(user) # Flask
      else:
        flash(u'Invalid Password Provided','login_error') # 
        return redirect("/") # just URL

    else:
      flash(u'User Is not yet registered','login_error')
      flash(u'username is incorrect!','login_error')
      return redirect("/") # just URL

  # return redirect("/timeline", user=user.id)
  return redirect(url_for('landing', id=user.id)) # to go to route directly and it is allowed to put only one argument

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect("/") # just URL

@login_manager.user_loader # checking the user and its id, so that it can access the /timeline
def load_user(id):         # this means checking the id of the user that can access the /timeline
  return User.query.get(int(id)) # flask wants to know the current data

@app.route("/landing")
def landing():

  # posts = Posts.query.filter_by().all()
  posts = Posts.query.filter().order_by(Posts.update_at.desc()).all()
  

  return render_template("landing.html", posts=posts) # URL and to pass the data

@app.route("/post", methods=['GET', 'POST', 'DELETE', 'PUT'])
def post():

  if request.method == "GET":
    pass
    # try: # try and expect to check if there is data on user.id
    post = Posts.query.filter_by(id=request.args.get("postid")).first() # will return only one user data
    return jsonify(postid=post.id, name=post.name, content=post.content, image=post.image)

    # except AttributeError: # we will return the whole data at the users
    #   posts = Posts.query.all()
    #   postlist = []
    #   for post in posts:
    #     posttoadd = {
    #       "id": post.id,
    #       "user_id": post.user_id,
    #       "name": post.name,
    #       "content": post.content,
    #       "image": post.image
    #     }
    #     postlist.append(posttoadd)

    #   return jsonify(postlist=postlist)

  elif request.method == "POST":
    files = request.files["image"]
    filename = files.filename

    files.save("static/" + filename)
    
    user_id = current_user.id
    name = request.form["name"]
    content = request.form["content"]
    image = filename

    post = Posts(user_id=user_id, name=name, content=content, image=image) # encryption
    db.session.add(post)  # inserting to the table
    db.session.commit()   # commit

    return redirect(url_for('landing', id=user_id))

  elif request.method == "DELETE": # Delete
    postid = request.form["postid"]

    post = Posts.query.filter_by(id=postid).first()
    db.session.delete(post)
    db.session.commit()   # commit

    return redirect(url_for('landing', id=current_user.id))

  elif request.method == "PUT": # Upadate

    files = request.files["image"]
    filename = files.filename

    files.save("static/" + filename)
    
    user_id = current_user.id
    name = request.form["updatepostname"]
    content = request.form["updatecontent"]
    image = filename

    postid = request.form["updatepostid"]
    post = Posts.query.filter_by(id=postid).first()
    post.user_id = user_id
    post.name = name
    post.content = content
    post.image = image

    db.session.commit()   # commit

    return redirect(url_for('landing', id=current_user.id))

@app.route("/updatePost/<int:id>")
def updatePost(id):
  post = Posts.query.filter_by(id=id).first()
  db.session.delete(post)
  db.session.commit()   # commit

  return redirect(url_for('landing', id=id))

@app.route("/deletePost/<int:id>")
def deletePost(id):
  post = Posts.query.filter_by(id=id).first()
  db.session.delete(post)
  db.session.commit()   # commit

  return redirect(url_for('landing', id=id))

@app.route("/item/<int:id>")
# @app.route("/item")
def item(id):
  # print(id)
  post = Posts.query.filter_by(id=id).first() 

  return render_template("item.html", post=post) # URL and to pass the data

@app.route("/review/<int:id>")
def review(id):
  # post = Posts.query.filter_by(id=id).order_by(Posts.update_at.desc()).first()
  post = Posts.query.filter_by(id=id).first()

  count = 0
  for i in post.reviews:
    count = count + i.score
  try:
    summary = count / len(post.reviews)
  except ZeroDivisionError:
    summary = 0

  return render_template("review.html", post=post, summary=summary) # URL and to pass the data

@app.route("/review2", methods=['GET', 'POST', 'DELETE', 'PUT'])
def review2():

  if request.method == "GET":
    pass
    # try: # try and expect to check if there is data on user.id
    #   post = Posts.query.filter_by(id=id).first()
    #   return render_template("item.html", post=post) # URL and to pass the data

    # except AttributeError: # we will return the whole data at the users
    #   posts = Posts.query.all()
    #   postlist = []
    #   for post in posts:
    #     posttoadd = {
    #       "id": post.id,
    #       "user_id": post.user_id,
    #       "name": post.name,
    #       "content": post.content,
    #       "image": post.image
    #     }
    #     postlist.append(posttoadd)

    #   return jsonify(postlist=postlist)

  elif request.method == "POST":
    user_id = current_user.id
    item_id = request.form["item_id"]
    title = request.form["title"]
    content = request.form["content"]
    score = request.form["radio"]

    review = Reviews(user_id=user_id, item_id=item_id, title=title, content=content, score=score) # encryption
    db.session.add(review)  # inserting to the table
    db.session.commit()   # commit

  return redirect(url_for('review', id=item_id))