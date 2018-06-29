# coding=utf-8

from functools import wraps
from flask import request, jsonify

from app.json_response import JsonResponse


class FlaskRequestCheck(object):

    @classmethod
    def check_args(cls, *args):
        """
        :return Boolean:

        usage:
        ```
        FlaskRequestCheck.check_args("username", "password")
        ```

        """
        return (set(request.args.keys()) & set(args)) == set(args)

    @classmethod
    def check_values(cls, *args):
        """
        :return Boolean:

        usage:
        ```
        FlaskRequestCheck.check_values("username", "password")
        ```

        """
        return (set(request.values.keys()) & set(args)) == set(args)

    @classmethod
    def check_values_decorator(cls, *args):
        """
        decorator
        检查 request.values 的参数
        """

        def _func(func):
            if not cls.args_check(args):
                return jsonify(JsonResponse.make_parameter_missing())

            @wraps(func)
            def wrapper(*args, **kw):
                ret = func(*args, **kw)
                return ret

            return wrapper
        return _func
