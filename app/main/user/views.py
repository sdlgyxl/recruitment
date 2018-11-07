#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 10:16
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : views.py
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from app import db
from .forms import EditUserForm, AddUserForm, TestForm
from app.models.user import User
from app.models.dept import Dept

from app.libs.redprint import Redprint
rp = Redprint('user')

@rp.route("/")
def list():
    return "user list"

@rp.route("/add", methods=['GET', 'POST'])
def add():
    form = AddUserForm()
    return render_template('main/user/edit.html', form=form)

@rp.route("/edit/<id>")
def edit(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        #user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@rp.route("/delete/<id>")
def delete(id):
    return "name = %s" % id



@rp.route("/test/")
def test():
    #name = None
    depts=Dept.query.all()
    form = TestForm()
    # 如果提交的数据验证通过，则返回True
    #if form.validate_on_submit():
    #    name = form.name.data
    #    form.name.data = ''
    return render_template('main/user/test.html', form=form, depts=depts)
