# encoding: utf-8
from schools.views import SchoolView, SchoolHomeView, SchoolCourseView, SchoolDescView, SchoolLecturerView, \
     LecturerListView, LecturerDetailView

__author__ = 'Shirlesha'
__date__ = '2019/5/12 0009 08:02'

from django.urls import path, re_path

app_name = "schools"

urlpatterns = [

    # 课程学校列表url
    path('list/', SchoolView.as_view(), name="school_list"),

    # # 添加我要学习
    # path('add_ask/', AddUserAskView.as_view(), name="add_ask"),

    # home页面,取纯数字
    re_path('home/(?P<school_id>\d+)/', SchoolHomeView.as_view(), name="school_home"),

    # 访问课程
    re_path('course/(?P<school_id>\d+)/', SchoolCourseView.as_view(), name="school_course"),

    # 访问学校描述
    re_path('desc/(?P<school_id>\d+)/', SchoolDescView.as_view(), name="school_desc"),

    # 访问学校讲师
    re_path('school_lecturer/(?P<school_id>\d+)/', SchoolLecturerView.as_view(), name="school_lecturer"),

    # # 学校收藏
    # path('add_fav/', AddFavView.as_view(), name="add_fav"),

    # 讲师列表
    path('lecturer/list/', LecturerListView.as_view(), name="lecturer_list"),

    # 访问学校讲师
    re_path('lecturer/detail/(?P<lecturer_id>\d+)/', LecturerDetailView.as_view(), name="lecturer_detail"),
]
