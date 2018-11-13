#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 10:16
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : views.py
from datetime import datetime
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_, and_
from .forms import EditUserForm, AddUserForm, TestForm, UserSearchForm
from app import db
from app.models.user import User, Dept
from app.models.commons import Privilege
from app.libs.redprint import Redprint
rp = Redprint('user')
from app.decorators import role_required

@rp.route("/")
@rp.route("/index/", methods=['GET', 'POST'])
@login_required
@role_required("用户列表")
def user_index(query=None):
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '').strip()
    privi = current_user.get_privilege("用户列表")
    c = current_user.can_see_users(privi)
    if query:
        query = query.replace("'", "")
        c = or_(User.name.like('%{}%'.format(query)), User.username.like('%{}%'.format(query)))
        c = or_(User.position.like('%{}%'.format(query)), c)
        c = and_(current_user.can_see_users(privi), c)
    users = User.query.filter(c).order_by(User.id)
    pagination = users.paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    #next_url = url_for('main.user_index', page=pagination.next_num, q=query) if pagination.has_next else None
    #prev_url = url_for('main.user_index', page=pagination.prev_num, q=query) if pagination.has_prev else None
    searchform=UserSearchForm()
    searchform.q.data = query
    return render_template('main/user/index.html', users=pagination.items, pagination=pagination,
                           title='用户列表', page=page, form=searchform, q=query)


@rp.route("/add", methods=['GET', 'POST'])
@login_required
@role_required("用户信息修改")
def user_add():
    form = AddUserForm()
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

@rp.route("/edit/<id>", methods=['GET', 'POST'])
def user_edit(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(id)
    form = EditUserForm(user=user)
    if form.validate_on_submit():
        photofile = None
        if form.photo.data:
            fileext = form.photo.data.filename.split('.')[-1]
            photofile = 'app/static/uploads/photo/' + str(datetime.now().timestamp()).replace('.', '') + '.' + fileext
            form.photo.data.save(photofile)
            photofile = photofile.replace('app/static/', '')
        user.id = form.id.data
        user.name = form.name.data
        user.username = form.username.data
        user.dept_id = form.dept.data
        user.superior = form.superior.data
        user.mobile = form.mobile.data
        user.email = form.email.data
        user.birthday = form.birthday.data
        user.entrydate = form.entrydate.data
        user.position = form.position.data
        user.office_location = form.office_location.data
        user.job_state = form.job_state.data
        user.profile = form.profile.data
        user.photo = photofile
        user.can_login = form.can_login.data
        user.is_manager = form.is_manager.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('main.user_index', page=page))
    form.id.data = user.id
    form.name.data = user.name
    form.username.data = user.username
    form.dept.data = user.dept
    form.superior.data = user.superior
    form.mobile.data = user.mobile
    form.email.data = user.email
    form.birthday.data = user.birthday
    form.entrydate.data = user.entrydate
    form.position.data = user.position
    form.office_location.data = user.office_location
    form.job_state.data = user.job_state or 0
    form.profile.data = user.profile
    form.photo.data = user.photo
    form.can_login.data = user.can_login
    form.is_manager.data = user.is_manager

    return render_template('main/user/edit.html', form=form, user=user)

@rp.route("/delete/<id>")
def user_delete(id):
    return "name = %s" % id

@rp.route("/updatepassword", methods=['GET', 'POST'])
def user_update_password():
    id = request.args.get('id', 1, type=int)
    password = request.args.get('password', 1, type=str)
    if current_user.cando("用户密码修改", id):
        return jsonify({"id": 9999, "password": "okokokok"})
    return jsonify({"id": id, "password": "error"})


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

