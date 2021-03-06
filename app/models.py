from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        """
        :param password:
        :return: the hash_password
        """
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        """
        :param password:
        :return: verify password equal old password
        """
        return custom_app_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer('test', expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('test')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    like = db.Column(db.Integer)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    posts = db.relationship("Post", backref="tag")


class View(db.Model):
    __tablename__ = "views"
    view_count = db.Column(db.Integer, primary_key=True)
