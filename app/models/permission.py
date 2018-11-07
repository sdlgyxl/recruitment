#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 9:08
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : user.py
from datetime import datetime, timedelta
from app import db, login
from flask_login import UserMixin
from .commons import PaginatedAPIMixin


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    privilege = db.Column(db.Integer)
