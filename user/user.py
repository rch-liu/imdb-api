# Inspired by https://gist.github.com/jslvtr/139cf76db7132b53f2b20c5b6a9fa7ad
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash
import json

class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class User:
  def __init__(self, username, password):
    self.username = username
    self.password = password
  
  def save_to_db(self):
    """
    Saves a new user object to the db.
    """
    hashedPswrd = generate_password_hash(self.password)
    cur = g.db.cursor()
    cur.execute(
      "INSERT INTO users VALUES (%s, %s)",
      (self.username, hashedPswrd,)
    )
    g.db.commit()


  @staticmethod
  def find_by_username(username):
    """
    Attempts to find the user given their username.
    This function returns the queried user object; if it doesn't exist, it returns None.
    """
    cur = g.db.cursor()
    cur.execute(
      "SELECT user_id, password FROM users WHERE user_id=(%s)",
      (username,)
    )
    res = cur.fetchone()
    return res

  @staticmethod
  def validate_password(given_password, user_password):
    """
    Determines if the password the user has provided is the same as
    the hashed password from the db.
    """
    return check_password_hash(user_password, given_password)
