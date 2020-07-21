# export FLASK_APP=run.pi
# flask shel

from .models import User, Categories, Posts, Reviews, PostLike

__all__ = [
  "User",
  "Categories",
  "Posts",
  "Reviews",
  "PostLike"
] # to access the table from view.py
