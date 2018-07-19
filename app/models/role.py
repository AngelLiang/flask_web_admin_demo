# coding=utf-8

from app.database import (db, SurrogatePK, CRUDMixin,
                          Model, reference_col, relationship)


class Role(Model, SurrogatePK):
    """Role model"""
    __tablename__ = 'roles'
    name = db.Column(db.String(80), unique=True,
                     index=True, nullable=False)  # 角色名称
    description = db.Column(db.String(255))  # 角色描述

    def __repr__(self):
        # return '<Role %r>' % self.name
        return self.name

    @classmethod
    def init_role(cls):
        admin = cls.get_or_create(name=u"管理员")
        developer = cls.get_or_create(name=u"开发者")
        default = cls.get_or_create(name=u"默认")

        return admin, developer, default
