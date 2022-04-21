import datetime

import sqlalchemy
from flask_login import UserMixin

from ..db_session import SqlAlchemyBase  # noqa


class PreRegisteredUser(SqlAlchemyBase, UserMixin):
    __tablename__ = 'pre_registered_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
