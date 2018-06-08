# cofing=utf-8

from flask import redirect, url_for, current_app
from flask_user import current_user

from . import views


@views.route('/')
@views.route('/index')
@views.route('/home')
def index():
    return redirect(url_for("admin.index"))
