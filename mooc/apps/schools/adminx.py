# encoding: utf-8
__author__ = 'Shirlesha'
__date__ = '2019/5/12 0009 08:02'

import xadmin

from .models import CityDict, SchoolName, Lecturer


class CityDictAdmin(object):
    """学校所属城市名后台管理器"""
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class SchoolNameAdmin(object):
    """学校课程信息管理器"""
    list_display = ['name', 'desc', 'category', 'add_time']
    search_fields = ['name', 'desc', 'category']
    list_filter = ['name', 'desc', 'category', 'city__name', 'address', 'add_time']


class LecturerAdmin(object):
    """讲师后台管理器"""
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(SchoolName, SchoolNameAdmin)
xadmin.site.register(Lecturer, LecturerAdmin)
