#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 9:29
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : officelocation.py

from flask import current_app, url_for


class OfficeLocation:
    莱芜 = 10
    济南 = 20
    北京 = 30
    上海 = 40

class JobState:
    试用 = 0
    正式 = 1
    实习 = 5
    停薪留职 = 10
    产假 = 11
    长假 = 12
    离职 = 20


class Privilege:
    禁止 = 0
    本人 = 1
    本部门 = 2
    本部门及所有下级部门 = 3
    全部 = 4

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data