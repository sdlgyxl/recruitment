#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 10:49
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, IntegerField, DateField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from app.models.user import User
from app.models.dept import Dept
from app.models.commons import OfficeLocation, JobState
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed

office_location_list = []
for each in vars(OfficeLocation):
    if '_' not in each:
        office_location_list.append((OfficeLocation.__dict__[each], each))

job_state_list = []
for each in vars(JobState):
    if '_' not in each:
        job_state_list.append((JobState.__dict__[each], each))

class AddUserForm(FlaskForm):
    id = IntegerField("工号", render_kw = {"placeholder": "4位整数"})
    name = StringField('姓名', validators=[DataRequired(), Length(2, 4)], render_kw = {"placeholder": "2至4个汉字"})
    username = StringField('用户名',
                           validators=[
                               DataRequired(), Length(2, 20),
                               Regexp('^[A-Za-z][A-Za-z.]*$', 0, '用户名只能使用英文字母')],
                           render_kw = {"placeholder": "2至20位英文字母"})
    dept = SelectField('部门', coerce=int)
    superior = SelectField('上级', coerce=int)
    password = StringField("密码", validators=[DataRequired(), Length(8, 8), Regexp('^[1-9][0-9]{7}', 0, '必须是8位数字')], render_kw = {"placeholder": "8位数字"})
    mobile = StringField('手机号',
                         description='* 网站不会泄露您的手机号',
                         validators=[Regexp('(1[3-9][0-9]{9}){0,1}', 0, '手机号必须是11位数字')],
                         render_kw = {"placeholder": "请输入手机号"})
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email(message=u"邮件格式有误")], render_kw={"placeholder": "E-mail: yourname@example.com"})
    birthday = DateField("出生日期", default='', format='%Y-%m-%d', validators=[DataRequired()])
    entrydate = DateField("入职日期", default='', format='%Y-%m-%d', validators=[DataRequired()])
    position = StringField('职务', validators=[DataRequired(), Length(2, 20)])
    office_location = SelectField("办公地点", coerce=int, choices = office_location_list, validators=[DataRequired()])
    job_state = SelectField("工作状态", coerce=int, choices = job_state_list)
    profile = TextAreaField("个人简介", render_kw={"style": "height:120px"})
    photo = FileField("照片", validators=[FileAllowed(['jpg', 'png', 'gif'], '只能是.jpg .gif .png格式')])
    can_login = RadioField("登录状态", coerce=int, choices = [(1, '允许登录'), (0, '禁止登陆')], default=1, render_kw={"class" : "form-inline"} )
    is_manager = RadioField("部门经理", coerce=int, choices = [(0, '职员'), (1, '经理')], default=0)
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.dept.choices = [(dept.id, dept.name)
                             for dept in Dept.query.order_by(Dept.superior, Dept.id).all()]
        self.superior.choices = [(superior.id, str(superior.id) + '--' + superior.name)
                             for superior in User.query.filter_by(is_manager = 1).order_by(User.superior, User.id).all()]


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
    photo = FileField("照片",
                      validators=[
                          # 文件必须选择;
                          FileRequired(),
                          #  指定文件上传的格式;
                          FileAllowed(['jpg', 'png', 'gif'], '只能是.jpg .gif .png格式')]
                      )
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
    #name = StringField('姓名', validators=[DataRequired()])
    #dept = StringField('部门')
    photo = FileField("照片",
                     validators=[
                         # 文件必须选择;
                         FileRequired(),
                         #  指定文件上传的格式;
                         FileAllowed(['jpg', 'png', 'gif'], '只能是.jpg .gif .png格式')]
                      )
    submit = SubmitField('确定')

