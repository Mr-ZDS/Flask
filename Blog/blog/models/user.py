from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from blog.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')
        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(128), nullable=False)
    blog_content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    blogger_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blogger = db.relationship('User', backref=db.backref('blogs'))
