#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-15 13:26
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, IntegerField, DateField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from app.models.user import User, Dept
from app.models.commons import *
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class CompanyForm(FlaskForm):
    id = StringField("公司编号", render_kw = {"readonly": "readonly"})
    companyname = StringField('公司名称', validators=[DataRequired(), Length(6, 20)])
    hr_name = StringField('用户姓名', validators=[DataRequired(), Length(2, 4)])
    username = StringField('用户名',
                           validators=[
                               DataRequired(), Length(2, 20),
                               Regexp('^[A-Za-z][A-Za-z.]*$', 0, '用户名只能使用英文字母')],
                           render_kw = {"placeholder": "2至20位英文字母"})
    password = StringField("密码", validators=[DataRequired(), Length(6, 20)])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email(message=u"邮件格式有误")],
                        render_kw={"placeholder": "E-mail: yourname@example.com"})
    mobile = StringField('手机号',
                         description='* 网站不会泄露您的手机号',
                         validators=[Regexp('(1[3-9][0-9]{9}){0,1}', 0, '手机号必须是11位数字')],
                         render_kw = {"placeholder": "请输入手机号"})
    industry = SelectField("所属行业", coerce=int, default=0, choices=IndustryChoices)
    userlevel = SelectField("企业等级", coerce=int, default=0, choices=UserLevelChoices)
    city_id = SelectField("所在地区", coerce=int, default=0, choices=CityChoices)
    location = StringField('详细地址', validators=[DataRequired(), Length(6, 20)])
    homepage = StringField('公司主页', validators=[DataRequired(), Length(6, 20)])
    consultant = SelectField("招聘顾问", coerce=int, default=0)
    cr_date = StringField("注册时间", render_kw = {"readonly": "readonly"})
    profile = TextAreaField("企业简介", render_kw={"style": "height:120px"})
    submit = SubmitField('保存')


    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.consultant.choices = [(consultant.id, consultant.name)
                             for consultant in User.query.order_by(User.superior, User.id).all()]


class EditCompanyForm(CompanyForm):
    password = None

    def __init__(self, company, *args, **kwargs):
        super(EditCompanyForm, self).__init__(*args, **kwargs)
        self.company = company


class SearchForm(FlaskForm):
    q = StringField('搜索', validators=[DataRequired()])