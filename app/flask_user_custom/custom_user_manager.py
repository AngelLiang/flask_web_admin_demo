# coding=utf-8
"""

usage:

本文件放在`app/custom_flask_user`文件夹下，然后在`app/__init__.py`初始化:

```
from .custom_flask_user.custom_user_manager import CustomUserManager
user_manager = CustomUserManager()
```

"""

from flask import current_app
from flask_user import UserManager
from app.exception import TokenTimeOutException
# from .custom_login_form import CustomLoginForm


class CustomUserManager(UserManager):
    """客制化UserManager"""

    def __init__(self, app=None, db=None, UserClass=None, **kwargs):
        super(CustomUserManager, self).__init__(app, db, UserClass, **kwargs)

    def customize(self, app):
        """
        flask-user 的 UserManager 客制化
        """

        self.app = app

        #######################################################################
        # 表单
        # self.LoginFormClass = CustomLoginForm

        #######################################################################
        # 客制化 flask-login 的 login_manager
        # self.login_manager

        # default
        # @self.login_manager.user_loader
        # def load_user_by_user_token(user_token):
        #     user = self.db_manager.UserClass.get_user_by_token(user_token)
        #     return user

        #######################################################################
        # 客制化 self.login_manager.request_loader
        @self.login_manager.request_loader
        def request_loader(request):
            user = None

            # 下面是一个认证链，可以设计成责任链模式

            # 从header获取
            api_key = request.headers.get('Authorization') or\
                request.headers.get('APIKEY')
            if api_key:
                current_app.logger.debug("get api key from header")
                # TODO:
                # user = self.db_manager.UserClass.get_user_by_apikey(api_key)
                return user

            # 从URL获取
            api_key = request.args.get('api_key')
            if api_key:
                current_app.logger.debug("got api key form query string")
                # TODO:
                # user = self.db_manager.UserClass.get_user_by_apikey(api_key)
                return user

            # 从表单获取
            token = request.values.get("token")
            if token:
                current_app.logger.debug("got token")
                try:
                    data = self.db_manager.UserClass.verify_token(token)
                except TokenTimeOutException:
                    return None
                else:
                    user_id = data.get("id")
                    if user_id:
                        user = self.db_manager.UserClass.query.get(id)
                        return user
            return None

        #######################################################################
        # 订阅 帐号登录 信号
        from flask_user.signals import user_logged_in

        @user_logged_in.connect_via(app)
        def _track_logins(sender, user, **extra):
            # TODO:
            current_app.logger.debug("{!r} login".format(user))
            user.login_info_update()

        #######################################################################
        # 其他信号
        from flask_user.signals import (user_logged_out, user_changed_password,
                                        user_registered, user_reset_password)
