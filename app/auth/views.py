#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 16:33
# @Author  : Sdlgyxl
# @Site    : MicroBLOG
# @File    : views.py

from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app import db
from app.auth import bp
from .forms import LoginForm
from app.models.user import User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('用户名或密码不正确')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='用户登录', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register')
def register():
    return 'register'

@bp.route('/reset_password_request')
def reset_password_request():
    return 'reset_password_request'