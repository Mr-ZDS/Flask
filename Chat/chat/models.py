import hashlib
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from chat.extensions import db, login_manager

class User(UserMixin,db.Model):
    email = db.Column(db.String(254), unique = True, nullable = False)
    nickname = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    github = db.Column(db.String(255))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    messages = db.relationship('Message', back_populates = 'author',cascade = 'all')

