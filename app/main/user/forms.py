#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 10:49
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from app.models.user import User
from app.models.dept import Dept

class AddUserForm(FlaskForm):
    id = IntegerField("工号")
    name = StringField('姓名', validators=[DataRequired(), Length(2, 3)])
    username = StringField('用户名', validators=[
        DataRequired(), Length(2, 20),
        Regexp('^[A-Za-z][A-Za-z.]*$', 0, '用户名只能使用英文字母')])
    #dept = SelectField('部门', coerce=int)
    #superior = SelectField('上级', coerce=int)
    '''
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    
    mobile = StringField('手机号', validators=[DataRequired(),
        Regexp('^1[3-9][3-9]{9}', 0, '手机号必须是11位数字')])
    
    password = StringField("密码", validators=[DataRequired(), Length(8, 8)])
    is_manager = BooleanField('是否经理')
    birthday = DateField("出生日期", validators=[DataRequired])
    entrydate = DateField("入职日期", validators=[DataRequired])
    position = StringField('职务', validators=[DataRequired(), Length(2, 20)])
    office_location = IntegerField("办公地点", validators=[DataRequired()])
    job_state = IntegerField("工作状态")
    can_login = BooleanField("允许登录")
    profile = StringField("个人简介")
    photo = StringField("照片")
    '''
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.dept.choices = [(dept.id, dept.name)
                             for dept in Dept.query.order_by(Dept.name).all()]
        #self.superior.choices = [(superior.id, superior.name)
        #                     for superior in User.query.order_by(User.name).all()]
        #self.user = user

class EditUserForm(AddUserForm):
    id = IntegerField("工号")
    name = StringField('姓名', validators=[DataRequired(), Length(2, 3)])
    username = StringField('用户名', validators=[
        DataRequired(), Length(2, 20),
        Regexp('^[A-Za-z][A-Za-z.]*$', 0, '用户名只能使用英文字母')])
    dept = SelectField('部门', coerce=int)
    superior = SelectField('上级', coerce=int)
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    mobile = StringField('手机号', validators=[DataRequired(),
                                            Regexp('^1[3-9][3-9]{9}', 0, '手机号必须是11位数字')])
    password = StringField("密码", validators=[DataRequired(), Length(8, 8)])
    is_manager = BooleanField('是否经理')
    birthday = DateField("出生日期", validators=[DataRequired])
    entrydate = DateField("入职日期", validators=[DataRequired])
    position = StringField('职务', validators=[DataRequired(), Length(2, 20)])
    office_location = IntegerField("办公地点", validators=[DataRequired()])
    job_state = IntegerField("工作状态")
    can_login = BooleanField("允许登录")
    profile = StringField("个人简介")
    photo = StringField("照片")
    submit = SubmitField('保存')

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.dept.choices = [(dept.id, dept.name)
                             for dept in Dept.query.order_by(Dept.name).all()]
        self.superior.choices = [(superior.id, superior.name)
                             for superior in User.query.order_by(User.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_mobile(self, field):
        if field.data != self.user.mobile and \
                User.query.filter_by(mobile=field.data).first():
            raise ValidationError('手机号已经存在')


class TestForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    dept = SelectField('部门', coerce=int, choices=[(1,'abc'),(2,'qwe')])
    submit = SubmitField('Submit')
