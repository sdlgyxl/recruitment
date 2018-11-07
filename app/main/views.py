#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 16:37
# @Author  : Sdlgyxl
# @Site    : MicroBLOG
# @File    : views.py
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')

@bp.route('/explore')
def explore():
    return 'explore'

