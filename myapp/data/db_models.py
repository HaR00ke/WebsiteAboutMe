import datetime
import sqlalchemy
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase  # noqa


def get_all_models():
    return [User, PreRegisteredUser, Achievment, Project, Contact]


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    password_requested_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_modified_date(self):
        self.modified_date = datetime.datetime.now()


class PreRegisteredUser(SqlAlchemyBase, UserMixin):
    __tablename__ = 'pre_registered_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class Achievment(SqlAlchemyBase):
    __tablename__ = 'achievments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def get_dict(self):
        ans = {'title': self.title, 'description': self.description}
        if self.img:
            ans['img'] = url_for('static', filename=f'img/uploaded/{self.img}')
        if self.url:
            ans['url'] = self.url
        return ans


class Project(SqlAlchemyBase):
    __tablename__ = 'projects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def get_dict(self):
        ans = {'title': self.title, 'description': self.description}
        if self.img:
            ans['img'] = url_for('static', filename=f'img/uploaded/{self.img}')
        if self.url:
            ans['url'] = self.url
        return ans


class Contact(SqlAlchemyBase):
    __tablename__ = 'contacts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def get_dict(self):
        return {'text': self.text, 'url': self.url}

# class Comment(SqlAlchemyBase):
#     pass