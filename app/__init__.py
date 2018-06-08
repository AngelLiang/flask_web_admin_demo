# coding=utf-8

import os
import sys
from flask import Flask, jsonify, url_for, request, current_app, session


# config
from config import config

curr_dir = os.path.dirname(os.path.realpath(__file__))

###############################################################################
# 数据库

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
from .database import db

###############################################################################
# 国际化

from flask_babelex import Babel
babel = Babel()


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'zh_CN')


###############################################################################
# cache
# 首选redis，次选进程内缓存

from werkzeug.contrib.cache import SimpleCache, RedisCache
try:
    cache = RedisCache()
    cache.get("connection")  # 连接测试
except Exception:
    cache = SimpleCache()
    print("cache is SimpleCache")
else:
    print("cache is RedisCache")

###############################################################################
# flask-user

try:
    from .custom_flask_user import CustomUserManager
    user_manager = CustomUserManager()
except Exception:
    from flask_user import UserManager
    user_manager = UserManager(None, None, None)

print("user_manager creata by {}".format(user_manager.__class__.__name__))

###############################################################################
# flask admin

from flask_admin import Admin
from app.views import init_admin_views
from app.views.base_view import CustomAdminIndexView

amdin_index_view = CustomAdminIndexView(
    name="仪表盘",
    menu_icon_type="glyph",
    menu_icon_value="glyphicon-home",
)
admin = Admin(
    index_view=amdin_index_view,
    template_mode="bootstrap3",
    # name="flask web admin demo",
)
admin.base_template = "admin/base.jinja2"  # 改为app/templates/admin/base.jinja2
init_admin_views(admin)

###############################################################################
# toolbar

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension()

###############################################################################


def create_app(config_name):
    # app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 数据库
    db.init_app(app)
    db.app = app

    # 国际化
    babel.init_app(app)

    # flask-admin
    admin.init_app(app)
    admin.name = app.config.get("APP_NAME")

    # flask-user
    from app.models import User
    from config.config_flask_user import FlaskUserConfig
    app.config.from_object(FlaskUserConfig)  # 添加 FlaskUserConfig 配置
    app.config["USER_APP_NAME"] = app.config.get("APP_NAME")
    user_manager.init_app(app, db, User)

    # toolbar
    toolbar.init_app(app)

    # jinja2 env
    from app.jinja2_env import init_jinja2_env
    init_jinja2_env(app)

    # views
    from app.views import views
    app.register_blueprint(views)

    # error pages
    # from app.errors import init_errors_page
    # init_errors_page(app)
    amdin_index_view.init_errors_page(app)

    return app
