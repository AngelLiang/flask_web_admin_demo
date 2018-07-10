# coding=utf-8

from sqlalchemy import func
from flask import Flask, request, url_for, current_app
from flask_user import current_user

# db
from app.database import db, Column, reference_col, relationship

# model
from app.models import User, Role

# cache
from app.cache import cache


def get_count(model) -> int:
    return db.session.query(func.count('*')).select_from(model).scalar()


@cache.memoize(timeout=60)
def get_user_count() -> int:
    """
    获取 User 表的数量
    缓存 60s
    """
    return get_count(User)

##########################################################################


def init_jinja2_env(app: Flask):
    app.add_template_global(get_user_count, "get_user_count")
