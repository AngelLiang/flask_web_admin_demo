# coding=utf-8

import os
import sys
from flask import Flask, jsonify, url_for, request, current_app, session


# config
from app.config import config

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

from .cache import cache

###############################################################################
# flask-user

from .flask_user_custom import CustomUserManager
user_manager = CustomUserManager()

###############################################################################
# flask admin

from flask_admin import Admin
from app.flask_admin_views import init_admin_views
from app.flask_admin_views.base_view import CustomAdminIndexView

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



    # database
    db.init_app(app)
    db.app = app

    # cache
    from app.cache import CachingConfig, cache
    app.config.from_object(CachingConfig)
    cache.init_app(app)

    # 国际化
    babel.init_app(app)

    # flask-admin
    admin.init_app(app)
    admin.name = app.config.get("APP_NAME")

    # flask-user
    from app.models import User
    from app.flask_user_custom import FlaskUserConfig
    app.config.from_object(FlaskUserConfig)  # 添加 FlaskUserConfig 配置
    app.config["USER_APP_NAME"] = app.config.get("APP_NAME")
    user_manager.init_app(app, db, User)

    # toolbar
    # toolbar.init_app(app)

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

    # apis
    from app.apis import api
    app.register_blueprint(api, url_prefix="/api/v1_0")

    # 慢查询日志
    from app.database import init_app
    init_app(app)

    return app
