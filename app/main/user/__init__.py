#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 10:15
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : __init__.py.py

from flask import Blueprint

bp = Blueprint('user', __name__)

from . import views