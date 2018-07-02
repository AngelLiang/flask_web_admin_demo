# coding=utf-8
"""
基于Flask的json response生成类
"""

from flask import request


class AbstractStatus(object):
    """
    状态抽象类
    """
    status = 0
    message = "message"
    data = {}

    def __init__(self, message=None, data=None):
        if message:
            self.message = message
        if data:
            self.data = data

    def to_dict(self, add_url=True):
        d = dict(status=self.status, message=self.message, data=self.data)
        if add_url:
            d["request"] = request.base_url
        return d


class StatusSuccess(AbstractStatus):
    status = 1
    message = "success!"


class StatusFail(AbstractStatus):
    status = 0
    message = "fail!"


class StatusParameterMiss(AbstractStatus):
    status = -1
    message = "parameter is missing!"


class StatusParameterError(AbstractStatus):
    status = -1
    message = "parameter is error!"


class JsonResponse(object):
    """
    usage:

    ```
    JsonResponse.make_success()
    ```

    """

    ##########################################################################
    # make method

    @classmethod
    def make_success(cls, data=None) -> dict:
        d = StatusSuccess(data=data).to_dict()
        return d

    @classmethod
    def make_fail(cls, message=None, data=None) -> dict:
        d = StatusFail(message=message, data=data).to_dict()
        return d

    @classmethod
    def make_parameter_miss(cls, data=None) -> dict:
        d = StatusParameterMiss(data=data).to_dict()
        return d

    @classmethod
    def make_parameter_error(cls, data=None) -> dict:
        d = StatusParameterError(data=data).to_dict()
        return d
