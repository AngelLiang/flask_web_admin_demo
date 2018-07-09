# coding=utf-8

from flask import jsonify, request, session, current_app, Blueprint
from flask.views import MethodView
from flask_user import current_user, login_required

from app import cache
from app.utils.json_response import JsonResponse as s_json
from app.utils.flask_request_check import FlaskRequestCheck as s_check


# model
from app.models import User

from app.exception import TokenTimeOutException

from . import api



@api.route("user/login", methods=["POST"])
def login():
    # 检测参数
    if not s_check.check_values("username", "password"):
        return(jsonify(s_json.make_parameter_miss()))

    values = request.values
    current_app.logger.debug(values)
    
    # 获取用户
    user = User.query.filter_by(username=values.get("username")).first()
    if user:
        ret = user.verify_password(values.get("password"))
        if ret: # 成功
            return jsonify(s_json.make_success(data=user.to_dict()))
        else:
            current_app.logger.debug("{} password error!".format(user))
            return jsonify(s_json.make_fail(message="password error!"))
    else:
        current_app.logger.debug("user not found!")

    return jsonify(s_json.make_fail())



@api.route("user/logout", methods=["POST"])
def logout():
    return jsonify(s_json.make_success())



@api.route("user/token/verify", methods=["GET", "POST"])
def verify_token():
    # 检测参数 
    if not s_check.check_values("token"):
        return jsonify(s_json.make_parameter_miss()) 
    # 获取token
    token = request.values.get("token")

    # 验证token
    try:
        data = User.verify_token(token)
    except TokenTimeOutException:
        return jsonify(s_json.make_fail(message="token timeout!"))
    else:
        user_id = data.get("id")
        if user_id:
            user = User.query.get(user_id)
            if user:    # 验证成功
                return jsonify(s_json.make_success(data=user.to_dict(has_token=False)))
    return jsonify(s_json.make_fail())

