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


class Dept(db.Model):
    __tablename__ = 'depts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    superior = db.Column(db.Integer, db.ForeignKey('depts.id'))
    is_active = db.Column(db.Boolean)
    cr_date = db.Column(db.Date)
    cancel_date = db.Column(db.Date)
    '''
    def __init__(self, **kwargs):
        super(Dept, self).__init__(**kwargs)
        if self.cr_date is None:
            self.cr_date = datetime.now()
    '''