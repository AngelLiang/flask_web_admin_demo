# coding=utf-8

import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):

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

    def test_index_page(self):
        """测试主页"""
        # response = self.client.get(url_for("views.index"))
        response = self.client.get("/", follow_redirects=True)
        # self.assertTrue(response.status_code == 302)    # 跳转
        # self.assertTrue("/admin/" in response.get_data(as_text=True))
        self.assertTrue(u"登录" in response.get_data(as_text=True))

    def test_register_and_login(self):
        """测试注册和登录"""
        username = "test_account"
        password = "Test123"    # 密码须包含至少6个字符，其中至少1个小写字母，1个大写字母和1个数字

        # 注册新账户
        response = self.client.post("/user/register", data={
            'username': username,
            'password': password,
            'retype_password': password
        })
        self.assertTrue(response.status_code == 302)

        # 使用新注册的账户登录
        response = self.client.post("/user/login", data={
            'username': username,
            'password': password
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search("test", data))
        self.assertTrue(u"登录成功" in data)

    @unittest.skip("don't test!")
    def test_skip():
        pass
