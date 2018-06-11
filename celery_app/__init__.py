# coding=utf-8
"""
celery -A celery_app:celery worker -l info

usage:

1、打开Python Console，导入该Python文件：import celery_demo
2、输入以下命令
>>> result = add.delay(23, 42)
>>> result.wait()

"""
from flask import Flask
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# app = Flask(__name__)
from wsgi import app

app.config.update(
    # Redis
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',

    # RabbitMQ
    # CELERY_BROKER_URL='amqp://guest:guest@localhost:5672//',
    # CELERY_RESULT_BACKEND='amqp://guest:guest@localhost:5672//',
)

celery = make_celery(app)

from .tasks import *
