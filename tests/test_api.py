# coding=utf-8

import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.init_role()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # @unittest.skip("don't test!")
    def test_api_register_and_login(self):
        """测试API登陆"""
        username = "api_test"
        password = "Test123"    # 密码须包含至少6个字符，其中至少1个小写字母，1个大写字母和1个数字

        # 注册新账户
        response = self.client.post("/user/register", data={
            'username': username,
            'password': password,
            'retype_password': password
        })
        # self.assertTrue(response.status_code == 302)

        # 使用新注册的账户登录
        response = self.client.post("/api/v1_0/user/login", data={
            'username': username,
            'password': password
        })
        data = response.get_json()
        # print(data)
        self.assertTrue(1 == data.get("status"))
