#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 9:08
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : user.py
from hashlib import md5
from datetime import datetime, timedelta
from app import db, login
from flask_login import UserMixin
from .commons import PaginatedAPIMixin
from random import SystemRandom
from werkzeug._compat import range_type, PY2, text_type, izip, to_bytes, string_types, to_native
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.commons import OfficeLocation, JobState

class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('depts.id'))
    dept = db.relationship('Dept', backref=db.backref('depts', lazy='dynamic'))
    superior = db.Column(db.Integer, db.ForeignKey('users.id'))
    superior_name = db.relationship("User", remote_side=[id], backref=db.backref('childs', lazy='dynamic'))
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    mobile = db.Column(db.String(11), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_manager = db.Column(db.Boolean)
    birthday = db.Column(db.Date)
    entrydate = db.Column(db.Date)
    position = db.Column(db.String(20))
    office_location = db.Column(db.Integer)
    job_state = db.Column(db.Integer)
    can_login = db.Column(db.Boolean)
    profile = db.Column(db.String(200))
    photo = db.Column(db.String(50))
    cr_date = db.Column(db.Date)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.cr_date is None:
            self.cr_date = datetime.now()\

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @property
    def manager_state(self):
        if self.is_manager == 1:
            return "经理"
        else:
            return "职员"

    @property
    def office(self):
        if not self.office_location:
            return ''
        for each in vars(OfficeLocation):
            if self.office_location == OfficeLocation.__dict__[each]:
                return each
        return ''

    @property
    def jobstate(self):
        if not self.job_state:
            return ''
        for each in vars(JobState):
            if self.job_state == JobState.__dict__[each]:
                return each
        return ''

    @property
    def loginstate(self):
        if self.can_login:
            return "登录"
        else:
            return "禁止"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))