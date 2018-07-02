# coding=utf-8

import os

curr_dir = os.path.abspath(os.path.dirname(__file__))
last_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app_dir = last_dir


class Config(object):
    APP_NAME = "基于Flask+Bootstrap后台演示"
    # SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY') or \
        'hard to guess string and longer than 32 byte!'

    # 数据库session在请求后自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 本地化
    BABEL_DEFAULT_LOCALE = "zh_CN"

    FLASK_ADMIN_THEME_FOLDER = "sb-admin-2"

    # toobar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'data-dev.sqlite')

    # If set to True,
    # Flask-SQLAlchemy will track modifications of objects and emit signals.
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # If set to True
    # SQLAlchemy will log all the statements issued to stderr
    # which can be useful for debugging.
    SQLALCHEMY_ECHO = False

    # jinja2模板自动加载
    TEMPLATES_AUTO_RELOAD = True

    # jinja2模板渲染跟踪
    EXPLAIN_TEMPLATE_LOADING = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'data-test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodection': ProductionConfig,
    'default': DevelopmentConfig
}
