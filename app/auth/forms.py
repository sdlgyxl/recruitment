#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 9:06
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.user import User