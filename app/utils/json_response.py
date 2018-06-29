# coding=utf-8
"""
基于Flask的json response生成类
"""

from flask import request


class AbstractStatus(object):
    """
    状态抽象类
    """
    @classmethod
    def to_dict(cls):
        return dict(status=cls.status, message=cls.message)


class StatusSuccess(AbstractStatus):
    status = 1
    message = "success!"


class StatusFail(AbstractStatus):
    status = 0
    message = "fail!"


class StatusParameterMissing(AbstractStatus):
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

    @staticmethod
    def add_data(d, data):
        if data is None:
            data = {}
        d.update(dict(data=data))

    @staticmethod
    def add_url(d):
        d.update(dict(request=request.base_url))

    @staticmethod
    def add_url_and_data(d, data):
        JsonResponse.add_url(d)
        JsonResponse.add_data(d, data)

    ##########################################################################
    # make method

    @classmethod
    def make_success(cls, data=None) -> dict:
        d = StatusSuccess.to_dict()
        cls.add_url_and_data(d, data)
        return d

    @classmethod
    def make_fail(cls, message=None, data=None) -> dict:
        d = StatusFail.to_dict()
        cls.add_url_and_data(d, data)
        if message:
            d.update({"message": message})
        return d

    @classmethod
    def make_parameter_missing(cls, data=None) -> dict:
        d = StatusParameterMissing.to_dict()
        cls.add_url_and_data(d, data)
        return d

    @classmethod
    def make_parameter_error(cls, data=None) -> dict:
        d = StatusParameterError.to_dict()
        cls.add_url_and_data(d, data)
        return d
