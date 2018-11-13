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
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.commons import OfficeLocation, JobState, Privilege

class Dept(db.Model):
    __tablename__ = 'depts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    superior = db.Column(db.Integer, db.ForeignKey('depts.id'))
    is_active = db.Column(db.Boolean)
    cr_date = db.Column(db.Date)
    cancel_date = db.Column(db.Date)
'''
Permission = db.Table('permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('privilege', db.Integer))
'''
class Permission(db.Model):
    __tablename__ = 'permissions'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    privilege = db.Column(db.Integer)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('depts.id'))
    dept = db.relationship('Dept', backref=db.backref('depts', lazy='dynamic'))
    superior = db.Column(db.Integer, db.ForeignKey('users.id'))
    superioruser = db.relationship("User", remote_side=[id], backref=db.backref('childs', lazy='dynamic'))
    #lowerusers = db.relationship("User", remote_side=[superior], backref=db.backref('childs', lazy='dynamic'))
    children = db.relationship("User", lazy="joined", join_depth=2)
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
    '''
    permissions = db.relationship('Permission',
                               backref=db.backref('permissions', lazy='joined'),
                               lazy='dynamic')
    '''

    roles = db.relationship('Role', secondary='permissions',
                              backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    permissions = db.relationship('Permission',
                               foreign_keys=[Permission.user_id],
                               backref=db.backref('r', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

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

    def hasrole(self, rolename):
        if self.get_role_id(rolename) > 0:
            return True
        return False

    def get_role_id(self, rolename):
        role_id = 0
        for r in self.roles:
            if r.name == rolename:
                role_id = r.id
                break
        return role_id

    def get_privilege(self, rolename):
        role_id = self.get_role_id(rolename)
        if role_id > 0:
            for p in self.permissions:
                if p.role_id == role_id:
                    return p.privilege
        return 0

    def can(self, rolename, privi):
        if self.get_privilege(rolename) >= privi:
            return True
        return False

    def haslower(self, userid):
        if userid == self.id:
            return False
        user = User.query.get(userid)
        while True:
            if not user:
                return False
            if user.id == self.id:
                return True
            user = user.superior_user

    def can_see_users(self, privi):
        from sqlalchemy import or_, and_
        if privi == Privilege.禁止:
            return and_(False)
        if privi == Privilege.本人:
            return and_(User.id==self.id)
        if privi == Privilege.本部门:
            return and_(User.dept_id==self.dept_id)
        if privi == Privilege.本部门及所有下级部门:
            str_proc = 'call procDeptsByAllLowersSelect(%d)' % self.dept_id
            deptids = db.session.execute(str_proc).fetchall()
            list_dept = deptids[0][0].split(',')
            list_dept.append(self.dept_id)
            return and_(User.dept_id.in_(list_dept))
        if privi == Privilege.全部:
            return and_(True)

    '''
    def can(self, perm, privi):
        for each in self.roles:
            if each.role_id == perm and each.privilege >= privi:
                return True
        return False
    '''


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''
class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    data = db.Column(db.String(50))
    children = db.relationship("Node", backref=db.backref('parent', remote_side=[id]), join_depth=4)
'''