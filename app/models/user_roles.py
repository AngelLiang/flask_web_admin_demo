# coding=utf-8

from app.database import (db, SurrogatePK, CRUDMixin,
                          Model, reference_col, relationship)


class UserRoles(db.Model):
    """User和Role的关联表"""
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)  # 必须加这一条，否则删除的时候sqlite会出错
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(),
                        db.ForeignKey('roles.id', ondelete='CASCADE'))
