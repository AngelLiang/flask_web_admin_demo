# coding=utf-8

from sqlalchemy import func
from flask import request, render_template, redirect, url_for, flash, current_app, session
from flask_user import login_required, roles_required, current_user
from flask_admin import Admin, expose

# db
from app.database import db, Column, reference_col, relationship

# model
from app.models import User, Role

# blueprint
from . import views

# flask admin base mode view
from .base_view import MyBaseModelView

##########################################################################
# 以下是一个view模板示例


class TemplateModelView(MyBaseModelView):
    pass


def init_admin_view(admin: Admin):
    admin.add_view(TemplateModelView(User, db.session, name=u"view模板",
                                     endpoint="endpoint", menu_icon_type="glyph",
                                     menu_icon_value="glyphicon-user",
                                     category="标签"))
