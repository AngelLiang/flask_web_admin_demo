# coding=utf-8

import time
from flask import current_app
from . import celery


@celery.task()
def add(a, b):
    return a + b


@celery.task()
def sleep(t):
    time.sleep(t)
