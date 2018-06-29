# coding=utf-8

import enum
import time
import random
import string
import hashlib
import datetime as dt

from flask import current_app, request
from flask_user import UserMixin, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

# database
from app import user_manager
from app.database import (db, SurrogatePK, CRUDMixin,
                          Model, reference_col, relationship)

# cache
from app.model_cache import ModelCacheMixin

# from .utils import enum_value_cb

# model


class SexEnum(enum.Enum):
    male = "男"
    female = "女"
    other = "其他"
    empty = ""


class UserRoles(db.Model):
    """User和Role的关联表"""
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)  # 必须加这一条，否则删除的时候sqlite会出错
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(),
                        db.ForeignKey('roles.id', ondelete='CASCADE'))


class Role(Model, SurrogatePK):
    """Role model"""
    __tablename__ = 'roles'
    name = db.Column(db.String(80), unique=True, index=True)  # 角色名称
    description = db.Column(db.String(255))  # 角色描述

    def __repr__(self):
        # return '<Role %r>' % self.name
        return self.description

    @classmethod
    def init_role(cls):
        admin = cls.get_or_create(name=u"管理员")
        developer = cls.get_or_create(name=u"开发者")
        default = cls.get_or_create(name=u"默认")

        return admin, developer, default


class User(Model, SurrogatePK, UserMixin, ModelCacheMixin):
    """user model"""
    __tablename__ = 'users'
    username = db.Column(db.String(32), unique=True,
                         index=True, nullable=False)  # username
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, default=None)  # Email
    phone = db.Column(db.String(32), index=True, default=None)
    sex = db.Column(db.Enum(SexEnum), default=SexEnum.empty)
    active = db.Column(db.Boolean(), default=True)
    nickname = db.Column(db.String(32), default="")  # 昵称
    avatar_hash = db.Column(db.String(32))  # 头像hash值

    current_login_datetime = db.Column(db.DateTime, nullable=True)  # 本次登录时间
    last_login_datetime = db.Column(db.DateTime, nullable=True)  # 上次登录时间
    last_login_ip = db.Column(db.String(32), nullable=True)  # 上次登录IP
    current_login_ip = db.Column(db.String(32), nullable=True)  # 当前登录IP

    create_datetime = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.now)  # 创建（注册）时间

    roles = db.relationship(
        'Role',
        secondary='user_roles',
        backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        """设置密码hash"""
        # for flask-user
        # from app import user_manager
        self.password_hash = user_manager.password_manager.hash_password(
            password)
        # for werkzeug
        # self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        # from app import user_manager
        return user_manager.password_manager.verify_password(
            password, self.password)

        # for werkzeug
        # return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        """生成头像"""
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.username.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def login_info_update(self, commit=True):
        """登录信息更新"""
        # import datetime as dt
        # from flask import request
        self.last_login_datetime = self.current_login_datetime
        self.current_login_datetime = dt.datetime.now()
        self.last_login_ip = self.current_login_ip
        self.current_login_ip = request.remote_addr
        db.session.add(self)
        if commit:
            db.session.commit()
