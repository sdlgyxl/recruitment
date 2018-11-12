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


class Module(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    module = db.Column(db.String(20))
    block = db.Column(db.String(20))
    point = db.Column(db.String(20))
