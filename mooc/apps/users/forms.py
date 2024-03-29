# encoding: utf-8
from captcha.fields import CaptchaField
from users.models import UserProfile

__author__ = 'Shirlesha'
__date__ = '2019/5/12 0009 08:02'

# 引入Django表单
from django import forms


class LoginForm(forms.Form):
    """登录表单验证"""
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    # 密码不能小于6位
    password = forms.CharField(required=True, min_length=6)


# 引入验证码field

class RegisterForm(forms.Form):
    """验证码form & 注册表单form"""
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    # 密码不能小于6位
    password = forms.CharField(required=True, min_length=6)
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ActiveForm(forms.Form):
    """激活时验证码实现"""
    # 激活时不对邮箱密码做验证
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    """忘记密码实现"""
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    """重置密码form实现"""
    # 密码不能小于6位
    password1 = forms.CharField(required=True, min_length=6)
    # 密码不能小于6位
    password2 = forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.ModelForm):
    """用于文件上传，修改头像"""
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """用于个人中心修改个人信息"""
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']
