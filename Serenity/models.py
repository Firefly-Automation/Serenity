# -*- coding: utf-8 -*-
# @Author: Zachary Priddy
# @Date:   2016-08-29 12:46:04
# @Last Modified by:   Zachary Priddy
# @Last Modified time: 2016-10-13 21:53:09

from Serenity import app


from flask import request
from flask.ext.security.decorators import _get_unauthorized_response
from flask_security import RoleMixin
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import UserMixin
from flask_security import auth_token_required
from flask_security import current_user
from flask_security.utils import encrypt_password
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from hashlib import sha256
from os import urandom


# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class AuthToken(db.Model):
  user_id = db.Column(db.String(255))
  token = db.Column(db.String(255), primary_key=True)
  app_name = db.Column(db.String(255))


class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Auth Token Check
def auth_token_required(fn):
  @wraps(fn)
  def decorated(*args, **kwargs):
    # return fn(*args, **kwargs)
    print request.get_json()
    rToken = request.get_json().get("token")
    argsToken = request.args.get('token')
    # return _get_unauthorized_response()
    for token in AuthToken.query.all():
      if rToken == token.token or argsToken == token.token:
        print token.user_id
        return fn(*args, **kwargs)
    return _get_unauthorized_response()
  return decorated

# Create a user to test with


@app.before_first_request
def create_user():
  adminUser = False
  db.create_all()
  for user in User.query.all():
    if user.email == 'admin':
      adminUser = True
  if not adminUser:
    user_datastore.create_user(
        email='admin', password=encrypt_password('FireflyPassword1234'))
    db.session.commit()


def add_user(username, password):
  userInDB = False
  for user in User.query.all():
    print user.email
    if user.email == username:
      userInDB = True
  if not userInDB:
    user_datastore.create_user(
        email=username, password=encrypt_password(password))
    db.session.commit()
    return True
  return False


def remove_user(username):
  userInDB = False
  userObject = None
  for user in User.query.all():
    print user.email
    if user.email == username:
      userInDB = True
      userObject = user
  if userInDB and username != 'admin':
    user_datastore.delete_user(userObject)
    db.session.commit()
    return True
  return False


def add_token(app_name):
  token = sha256(urandom(128)).hexdigest()
  db.session.add(AuthToken(user_id=str(current_user.id), token=token, app_name=app_name))
  db.session.commit()
  return token


def remove_token(token):
  AuthToken.query.filter_by(token=token).delete()
  db.session.commit()
