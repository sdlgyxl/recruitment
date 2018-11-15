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

OfficeLocationChoices = [(OfficeLocation.__dict__[x], x)
                         for x in vars(OfficeLocation) if '_' not in x]


class JobState:
    正式 = 1
    试用 = 5
    实习 = 7
    停薪留职 = 10
    产假 = 11
    长假 = 12
    离职 = 20


JobStateChoices = [(JobState.__dict__[x], x)
                   for x in vars(JobState) if '_' not in x]


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


class Industry:
    电子 = 1
    机械 = 2
    互联网 = 3
    交通 = 4
    行政 = 5

IndustryChoices = [(Industry.__dict__[x], x)
                   for x in vars(Industry) if '_' not in x]

class UserLevel:
    一级 = 1
    二级 = 2
    三级 = 3
    四级 = 4


UserLevelChoices = [(UserLevel.__dict__[x], x)
                   for x in vars(UserLevel) if '_' not in x]


class City:
    北京 = 1
    上海 = 2
    广州 = 3
    青岛 = 4


CityChoices = [(City.__dict__[x], x)
                    for x in vars(City) if '_' not in x]


