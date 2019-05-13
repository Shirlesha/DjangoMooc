# encoding: utf-8
import django

from users.views import UserInfoView, UploadImageView, SendEmailCodeView, UpdateEmailView, UpdatePwdView, MyCourseView, \
     MyFavLecturerView, MyFavCourseView, MyMessageView

__author__ = 'Shirlesha'
__date__ = '2019/5/12 0009 08:02'

from django.urls import path
app_name = "users"
urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name="user_info"),
    # 用户头像上传
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),
    # 用户个人中心修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    # 专用于发送验证码的
    path(
        'sendemail_code/',
        SendEmailCodeView.as_view(),
        name="sendemail_code"),
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),
    # 用户中心我的课程
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),

    # # 我收藏的课程机构
    # path('myfav/school/', MyFavSchoolView.as_view(), name="myfav_school"),

    # 我收藏的授课讲师
    path('myfav/lecturer/', MyFavLecturerView.as_view(), name="myfav_lecturer"),

    # 我收藏的课程
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息记录
    path('my_message/', MyMessageView.as_view(), name="my_message"),

]
