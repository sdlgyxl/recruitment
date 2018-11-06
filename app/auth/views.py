#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 16:33
# @Author  : Sdlgyxl
# @Site    : MicroBLOG
# @File    : views.py

from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'login'

@bp.route('/explore')
def explore():
    return 'explore'