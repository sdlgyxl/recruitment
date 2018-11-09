#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 10:16
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : views.py
from datetime import datetime
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask_login import current_user, login_required
from .forms import EditUserForm, AddUserForm, TestForm
from app import db
from app.models.user import User
from app.models.dept import Dept

from app.libs.redprint import Redprint
rp = Redprint('user')

@rp.route("/")
@rp.route("/index/")
def user_index():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.user_index', page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('main.user_index', page=pagination.prev_num) if pagination.has_prev else None
    return render_template('main/user/index.html', users=pagination.items, pagination=pagination,
                           title='用户列表', next_url=next_url, prev_url=prev_url)


@rp.route("/add", methods=['GET', 'POST'])
@login_required
def user_add():
    form = AddUserForm()
    print('form.birthday.data=', form.birthday.data)
    if form.validate_on_submit():
        photofile = None
        if form.photo.data:
            fileext = form.photo.data.filename.split('.')[-1]
            photofile = 'uploads/photo/' + str(datetime.now().timestamp()).replace('.', '') + '.' + fileext
            form.photo.data.save(photofile)
        user = User(id = form.id.data,
                    name = form.name.data,
                    dept_id = form.dept.data,
                    superior = form.superior.data,
                    username = form.username.data,
                    password = form.password.data,
                    email = form.email.data,
                    mobile = form.mobile.data,
                    is_manager = form.is_manager.data,
                    birthday = form.birthday.data.strftime('%Y-%m-%d'),
                    entrydate = form.entrydate.data.strftime('%Y-%m-%d'),
                    position = form.position.data,
                    office_location = form.office_location.data,
                    job_state = form.job_state.data,
                    can_login = form.can_login.data,
                    profile = form.profile.data,
                    photo = photofile,
                    cr_date = datetime.now())
        db.session.add(user)
        return redirect(url_for('main.user_add'))
    return render_template('main/user/edit.html', form=form)

@rp.route("/edit/<id>")
def user_edit(id):
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
def user_delete(id):
    return "name = %s" % id


@rp.route("/test/", methods=['GET', 'POST'])
def user_test():
    form = TestForm()
    messages = []
    # 如果提交的数据验证通过，则返回True
    if form.validate_on_submit():
        #name = form.name.data
        #form.name.data = ''
        filename = form.photo.data.filename
        form.photo.data.save('uploads/' + filename)
        messages.append(filename)
        #messages.append(name)
        return redirect(url_for('main.user_add'))
    return render_template('main/user/test.html', form=form, msg=messages)

