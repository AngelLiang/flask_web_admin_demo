# coding=utf-8

from flask import Blueprint

api = Blueprint("api", __name__)

from .user_api import init_api as init_user
init_user(api)
