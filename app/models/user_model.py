# coding=utf-8

import enum
import time
import random
import string
import hashlib
import datetime as dt

from flask import current_app, request
from flask_user import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.security import gen_salt
# database
from app import user_manager
from app.database import (db, SurrogatePK, CRUDMixin,
                          Model, reference_col, relationship)

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app.exception import TokenTimeOutException

# cache
from app.utils.model_cache import ModelCacheMixin

from .utils import enum_value_cb
from app.utils.compat import u, b2s

# model


class SexEnum(enum.Enum):
    male = "男"
    female = "女"
    other = "其他"
    empty = "未填"


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
    name = db.Column(db.String(80), unique=True,
                     index=True, nullable=False)  # 角色名称
    description = db.Column(db.String(255))  # 角色描述

    def __repr__(self):
        # return '<Role %r>' % self.name
        return self.name

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
    email = db.Column(db.String(128), default="")  # Email
    phone = db.Column(db.String(32), default="")
    # sex = db.Column(
    #     db.Enum(SexEnum,
    #             values_callable=enum_value_cb
    #             ), default=SexEnum.empty)
    sex = db.Column(db.String(8), default="")
    active = db.Column(db.Boolean(), default=True)
    nickname = db.Column(db.String(32), default="")  # 昵称
    avatar_hash = db.Column(db.String(32))  # 头像hash值

    current_login_datetime = db.Column(db.DateTime, default=None)  # 本次登录时间
    last_login_datetime = db.Column(db.DateTime, default=None)  # 上次登录时间
    last_login_ip = db.Column(db.String(32), default="")  # 上次登录IP
    current_login_ip = db.Column(db.String(32), default="")  # 当前登录IP

    create_datetime = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.now)  # 创建（注册）时间

    api_key = db.Column(db.String(128))

    roles = db.relationship(
        'Role',
        secondary='user_roles',
        backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<%s %r>'.format(self.__class__.__name__, self.username)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        """设置密码hash
        使用了 flask-user 则不能进行加密， 因为 flask-user 设置密码之前已经加密了
        """
        # for flask-user
        # from app import user_manager
        # self.password_hash = user_manager.password_manager.hash_password(password)
        self.password_hash = password

        # for werkzeug
        # self.password_hash = generate_password_hash(password)

    def gen_password(self, password):
        """
        为非注册的用户生成密码
        """
        self.password_hash = user_manager.password_manager.hash_password(
            password)

    def verify_password(self, password):
        """验证密码"""
        # from app import user_manager
        return user_manager.password_manager.verify_password(password, self.password_hash)

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
        if request:
            self.current_login_ip = request.remote_addr
        db.session.add(self)
        if commit:
            db.session.commit()

    def to_dict(self, has_token=True):

        data = {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "phone": self.phone,
            # "sex": repr(self.sex),
            "sex": self.sex,
            "active": self.active,
            "nickname": self.nickname,
            "create_datetime": self.create_datetime,
            "avatar": self.gravatar(),
            "roles": [role.name for role in self.roles],
        }
        if has_token:
            data.update({"token": self.generate_token()})
        return data

    def generate_token(self, expiration=60 * 60):
        """生成access token"""
        s = Serializer(current_app.config["SECRET_KEY"], expiration)

        # 把 id、username、roles 放进 token
        token = s.dumps({
            "id": self.id,
            "username": self.username,
            "roles": [role.name for role in self.roles]
        }).decode()

        return token

    @staticmethod
    def verify_token(token):
        """验证token
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            raise TokenTimeOutException
        except Exception:
            return None

        return data

    def gen_apikey(self):
        self.api_key = gen_salt(128)
