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
from app.company import bp
from app.decorators import role_required
from .forms import CompanyForm, EditCompanyForm, SearchForm
from app.models.job import Company, Job
from app.models.commons import *


@bp.route("/")
@bp.route("/index/", methods=['GET', 'POST'])
@login_required
#@role_required("企业查询")
def index(query=None):
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '').strip()
    privi = current_user.get_privilege("公司列表")
    if query:
        query = query.replace("'", "")
        c = (Company.name.like('%{}%'.format(query)), Company.profile.like('%{}%'.format(query)))
        companys = Company.query.filter(c).order_by(Company.id)
    companys = Company.query.order_by(Company.id)
    pagination = companys.paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    # next_url = url_for('main.user_index', page=pagination.next_num, q=query) if pagination.has_next else None
    # prev_url = url_for('main.user_index', page=pagination.prev_num, q=query) if pagination.has_prev else None
    searchform = SearchForm()
    searchform.q.data = query
    #print(len(pagination.items))
    return render_template('company/index.html', companys=pagination.items, pagination=pagination,
                           title='企业列表', page=page, form=searchform, q=query)


@bp.route("/add", methods=['GET', 'POST'])
def add():
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company()
        fill_company(company, form, 1)
        return redirect(url_for('company.add'))
    return render_template('company/company_edit.html', form=form)

#state 1 add; 2 edit
def fill_company(company, form, state):
    company.companyname = form.companyname.data
    company.hr_name = form.hr_name.data
    company.username = form.username.data
    company.email = form.email.data
    company.mobile = form.mobile.data
    company.profile = form.profile.data
    company.industry = form.industry.data
    company.userlevel = form.userlevel.data
    company.city_id = form.city_id.data
    company.location = form.location.data
    company.homepage = form.homepage.data
    if state == 1:
        company.state = 1
        company.reg_from = 1
        company.consultant = form.consultant.data
        company.cr_date = datetime.now()
        company.password = form.password.data
    db.session.add(company)


@bp.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id):
    company = Company.query.get_or_404(id)
    form = EditCompanyForm(company=company)
    if form.validate_on_submit():
        fill_company(company, form, 2)
        return redirect(url_for('company.add'))
    form.id.data = company.id
    form.companyname.data = company.companyname
    form.hr_name.data = company.hr_name
    form.username.data = company.username
    form.email.data = company.email
    form.mobile.data = company.mobile
    form.profile.data = company.profile
    form.industry.data = company.industry
    form.userlevel.data = company.userlevel
    form.city_id.data = company.city_id
    form.location.data = company.location
    form.homepage.data = company.homepage
    form.consultant.data = company.consultant
    form.cr_date.data = company.cr_date
    return render_template('company/company_edit.html', form=form)


@bp.route("/updatepassword", methods=['GET', 'POST'])
def update_password():
    id = request.args.get('id', 1, type=int)
    password = request.args.get('password', 1, type=str)
    company = Company.query.get(id)
    company.password = password
    return jsonify({"state": "已经成功修改密码"})
    