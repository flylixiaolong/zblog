"""
    auth: lixl
    mail: fly_lxl@fomail.com
    date: 2018-03-15
"""

from blog import db
from sqlalchemy import Column, Integer, String


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)
