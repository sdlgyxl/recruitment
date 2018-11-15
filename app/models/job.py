#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-15 11:28
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : job.py
from hashlib import md5
from datetime import datetime, timedelta
from app import db, login
from flask_login import UserMixin
from .commons import PaginatedAPIMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.commons import OfficeLocation, JobState, Privilege
from dateutil import rrule

class Company(db.Model):
    __tablename__ = 'companys'
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(20), index=True)
    hr_name = db.Column(db.String(20), index=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50), index=True, unique=True)
    mobile = db.Column(db.String(11), index=True, unique=True)
    profile = db.Column(db.String(500))
    industry = db.Column(db.Integer, index=True)
    userlevel = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    location = db.Column(db.String(50))
    homepage = db.Column(db.String(50))
    state = db.Column(db.Integer)
    reg_from = db.Column(db.Integer)
    logo = db.Column(db.String(50))
    consultant = db.Column(db.Integer, db.ForeignKey('users.id'))
    consultant_info = db.relationship('User', backref=db.backref('users', lazy='dynamic'))
    cr_date = db.Column(db.Date)
    jobs = db.relationship('Job', backref=db.backref('jobs', lazy='joined'), lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companys.id'))
    company = db.relationship('Company', backref=db.backref('companys', lazy='dynamic'))
    profile = db.Column(db.String(500))
    jobtype = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    online = db.Column(db.Date)
    offline = db.Column(db.Date)
    cr_date = db.Column(db.Date)
