# coding=utf-8

from flask_restless import APIManager


api_manager = APIManager()

# User
from app.models import User

api_manager.create_api(
    User, methods=['GET', 'POST', 'DELETE', "PUT"],
    url_prefix="/api/model"
)


from app.models import Role
api_manager.create_api(
    Role, methods=['GET', 'POST', 'DELETE'],
    url_prefix="/api/model"
)
