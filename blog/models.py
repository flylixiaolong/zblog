"""
    auth: lixl
    mail: fly_lxl@fomail.com
    date: 2018-03-15
"""

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash
from itsdangerous import JSONWebSignatureSerializer as JWT

from datetime import datetime

from blog import db
from blog import login_manager


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


from sqlalchemy import Column


class AbsUser(UserMixin, db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True,
                          unique=True, nullable=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=3600):
        jwt = JWT(current_app.config['SECRET_KEY'], expires_in=expiration)
        return jwt.dumps({'id': self.id, 'user_name': self.user_name, 'email': self.email}).decode()

    @staticmethod
    def verify_auth_token(token):
        jwt = JWT(current_app.config['SECRET_KEY'])
        try:
            data = jwt.loads(token)
        except:
            return None
        return Admin.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.user_name


class Admin(AbsUser):
    __tablename__ = 'auth_admin'
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.Enum('female', 'male'), nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)

    def has_perms(self, perms):
        pass

    def is_admin(self):
        return True


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    summary = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=False)
    created_id = db.Column(db.ForeignKey('auth_admin.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_id = db.Column(db.ForeignKey('auth_admin.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)