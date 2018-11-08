#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 15:32
# @Author  : Sdlgyxl
# @Site    : 公司后台
# @File    : aaa.py

class OfficeLocation:
    莱芜 = 10
    济南 = 20
    北京 = 30
    上海 = 40

officeList = []
for each in vars(OfficeLocation):
    if '_' not in each:
        officeList.append((OfficeLocation.__dict__[each], each))

print(officeList)