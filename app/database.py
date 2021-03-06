# coding=utf-8
"""
Flask 常用的 Model 抽象类
"""

import uuid
from flask import g, current_app
from app.utils.compat import string_types
# from six import string_types

from sqlalchemy import func, and_, or_
from sqlalchemy.orm import backref, aliased
from sqlalchemy.ext.declarative import as_declarative, declared_attr


# Alias common SQLAlchemy names
# from . import db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


Column = db.Column
relationship = db.relationship


def gen_uuid(prefix=""):
    return prefix + str(uuid.uuid4())


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def get_or_create(cls, q=None, **kwargs):
        """
        以指定参数进行查询，如果查询到则返回该对象
        如果没有查询到，则创建一个对象并返回

        usage:
        ```
        cls.get_or_create(q={"username":"admin"}, password="admin")
        cls.get_or_create(username="admin")
        ```

        """

        instance = None

        # 以指定参数进行查询
        if q:
            instance = cls.query.filter_by(**q).first()
        else:
            attr_list = [{attr: val} for attr, val in kwargs.items()]
            # 以 kwargs 排第一的参数进行查询
            # 因为Python3.5以前字典是无序，所以可能拿到的不是传参的第一个参数
            if len(attr_list) > 0:
                # print("attr_list", attr_list)
                q = attr_list[0]
                instance = cls.query.filter_by(**q).first()

        if not instance:
            if not q:
                q = {}
            q.update(kwargs)
            # print("q", q)
            instance = cls.create(**q)
            # print("create a " + str(instance))

        return instance


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    # def __init__(*args, **kwargs):
    #     pass


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(db.String(128), primary_key=True, default=gen_uuid)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any((isinstance(record_id, string_types) and record_id.isdigit(),
                isinstance(record_id, (int, float))), ):
            return cls.query.get(int(record_id))
        return None
        # return cls.query.get(record_id)


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)


##########################################################################
# 获取db链接，以下接口暂时用不到
# from: http://flask.pocoo.org/docs/1.0/tutorial/database/

def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row

        g.db = db

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

##########################################################################
# 慢查询日志


class SQLConfig(object):
    SQLALCHEMY_RECORD_QUERIES = True
    # slow database query threshold (in seconds)
    DATABASE_QUERY_TIMEOUT = 0.5


def init_app(app):
    from flask_sqlalchemy import get_debug_queries

    app.config.from_object(SQLConfig)
    timeout = SQLConfig.DATABASE_QUERY_TIMEOUT

    # 慢查询日志初始化
    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            if query.duration >= timeout:
                current_app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (
                    query.statement, query.parameters, query.duration, query.context))
        return response
