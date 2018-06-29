# coding=utf-8

from flask import jsonify, request, session, current_app, Blueprint
from flask.views import MethodView
from flask_user import current_user, login_required

from app import cache
from app.json_response import JsonResponse as s_json
from app.flask_request_check import FlaskRequestCheck as s_check


# model
from app.models import User


class UserAPIObj(object):

    def __init__(self, api=None):
        self.api = api

    def login(self):
        values = request.values
        current_app.logger.debug(values)

        ret = s_check.check_values("username", "password")
        if not ret:
            return(jsonify(s_json.make_parameter_missing()))

        user = User.query.filter_by(username=values.get("username")).first()
        if user:
            ret = user.verify_password(values.get("password"))
            if ret:
                return jsonify(s_json.make_success(data=user.to_dict()))
            else:
                current_app.logger.debug("{} password error!".format(user))
                return jsonify(s_json.make_fail(message="password error!"))
        else:
            current_app.logger.debug("user not found!")
        return jsonify(s_json.make_fail())

    def init_api(self, api: Blueprint):
        self.api = api
        api.add_url_rule("user/login", view_func=self.login, methods=["POST"])


def init_api(api: Blueprint):
    UserAPIObj().init_api(api)
