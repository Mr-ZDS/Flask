from blog.extensions import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    ques_time = db.Column(db.DateTime, default=datetime.now)
    blogger_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blogger = db.relationship('User', backref=db.backref('questions'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    answer_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer_name = db.relationship('User', backref=db.backref('answers'))
    question = db.relationship('Question', backref=db.backref('answers',
                                                              order_by=id.desc()))
