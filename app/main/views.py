#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 16:37
# @Author  : Sdlgyxl
# @Site    : MicroBLOG
# @File    : views.py
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        #g.search_form = SearchForm()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    name = "world"
    if not current_user.is_anonymous:
        name = current_user.name
    return render_template('main/index.html', title="首页", name=name)

@bp.route('/explore')
def explore():
    return 'explore'


