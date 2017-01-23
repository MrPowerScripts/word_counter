from app.extensions import db
import jwt
import json
import logging
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.dialects.postgresql import JSONB, DOUBLE_PRECISION, TEXT
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import backref
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, index=True)
    date_created = db.Column(db.DateTime, index=True,  server_default=utcnow())
    date_modified = db.Column(db.DateTime, index=True,  server_default=utcnow(),
                              onupdate=utcnow())


class URLS(Base):
    __tablename__ = "urls"

    url = db.Column(TEXT, unique=True, index=True)

    def __repr__(self):
        return '<urls {0}>'.format(self.id)


class URLContent(Base):
    __tablename__ = 'url_content'

    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), index=True)
    raw_content = db.Column(TEXT)
    text_content = db.Column(TEXT)
    word_counts = db.Column(TEXT)

    def __repr__(self):
        return '<url_content ({0})>'.format(self.id)
