# coding=utf-8
"""
gunicorn wsgi:app -c gunicorn_config.py
"""

import os
from flask.cli import load_dotenv
from app import create_app

load_dotenv()   # 显式加载 .flaskenv 和 .env

app = create_app("production")
