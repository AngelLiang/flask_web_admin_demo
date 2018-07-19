# coding=utf-8
"""

.flaskenv:

FLASK_APP=main.py
FLASK_ENV=development

"""

import os
from flask.cli import load_dotenv
from app import create_app

curr_dir = os.path.dirname(os.path.realpath(__file__))

# 使用 os.getenv('FLASK_ENV') 必须调用
# 当使用`python main.py`启动时需要手动加载环境
load_dotenv()   # 显式加载 .flaskenv 和 .env

app = create_app(os.getenv('FLASK_ENV') or 'default')


def run_profiler():
    # app.run()

    # 性能分析
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run(debug=True)


if __name__ == '__main__':
    # main()
    host = os.getenv("HOST") or app.config.get("HOST") or "127.0.0.1"
    port = os.getenv("PORT") or app.config.get("PORT") or 5000
    app.run(host=host, port=port)

###############################################################################

import getpass

from flask import current_app
from app import db
from app.models import User, Role


def _createuser(roles):
    username = input("Please Enter the superuser username:")
    if not username:
        print("username is empty!")
        return

    if User.query.filter_by(username=username).first():
        print("There is the same superuser username!")
        return

    password = getpass.getpass("Password:")
    password2 = getpass.getpass("Confirm password:")
    if password != password2:
        print("password is not confirmed!")
        return

    user = User.create(
        username=username, roles=roles, active=True)
    user.password = User.gen_password(password)
    return user


@app.cli.command()
def createsuperuser():
    """创建超级管理员"""

    roles = Role.init_role()
    ret = _createuser(list(roles))
    if ret:
        print("Superuser is created successfully!")


@app.cli.command()
def initdb():
    """数据库初始化"""
    db.create_all()
    print("The database is created successfully!")


@app.cli.command()
def dropdb():
    """清空数据库"""
    ret = input("drop the database? [y/n] ")
    if ret in ("y", "Y", "yes"):
        db.drop_all()


@app.cli.command()
def test():
    """测试用例"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()
