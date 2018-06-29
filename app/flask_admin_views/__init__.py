# coding=utf-8

from flask import Blueprint
from flask_admin import Admin

from .user_view import init_admin_view as init_user


def init_admin_views(admin: Admin):
    init_user(admin)
