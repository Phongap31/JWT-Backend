from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'accounts'

    id = db.Column('id',db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    email = db.Column(db.String())
    password = db.Column(db.String(), nullable = False)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(50), nullable = False)
    birthday = db.Column(db.Date, nullable = False)
    email = db.Column(db.String())
    level = db.Column(db.String(50))
