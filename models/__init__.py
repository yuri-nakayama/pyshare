# export FLASK_APP=run.pi
# flask shel

from .models import User, Posts, Reviews

__all__ = [
  "User",
  "Posts",
  "Reviews"
] # to access the table from view.py
