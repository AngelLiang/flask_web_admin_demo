# coding=utf-8

from flask import Blueprint

views = Blueprint("views", __name__, template_folder="templates")

from .index_views import *
