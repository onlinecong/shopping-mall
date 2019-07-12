import re

from django import forms
from django.core.exceptions import ValidationError

from userinfo.models import UserInfo
from captcha.fields import CaptchaField


# 验证密码不是纯数字
def check_password(value):
    if re.match(r'\d+', value):
        raise ValidationError('密码不能是纯数字')
# 验证手机号规则
def check_phone(value):
    if not re.match(r"^1[35678]\d{9}$",value):
        raise ValidationError('请输入合法的手机号')

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',min_length=3,error_messages={
        'required':'必须输入用户名',
        'min_length':'用户名长度不小于三个字符'
    })
    password = forms.CharField(label='密码',min_length=3,max_length=30,validators=[check_password],widget=forms.PasswordInput,error_messages={
        'required': '必须输入密码',
        'min_length': '密码长度不小于三个字符',
        'max_length':'密码长度不大于30个字符'
    })
    repassword = forms.CharField(label='确认密码',min_length=3,max_length=30,validators=[check_password],widget=forms.PasswordInput,error_messages={
        'required': '必须输入确认密码',
        'min_length': '密码长度不小于三个字符',
        'max_length':'密码长度不大于30个字符'
    })
    phone = forms.CharField(label='手机号',validators=[check_phone],error_messages={
        'required':'必须输入手机号',
    })

    # 验证用户名
    def clean_username(self):
        name = self.cleaned_data.get('username')
        res = UserInfo.objects.filter(username=name).exists()
        if res:
            raise ValidationError('用户名重复')
        else:
            return name
    # 两次密码输入一致
    def clean_pwd(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('repassword')
        if pwd1 != pwd2:
            raise ValidationError('两次密码必须一致')
        else:
            return pwd1

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=3, error_messages={
        'required': '必须输入用户名',
        'min_length': '用户名长度不小于三个字符'
    })
    password = forms.CharField(label='密码', min_length=3, max_length=30, validators=[check_password],
                               widget=forms.PasswordInput, error_messages={
            'required': '必须输入密码',
            'min_length': '密码长度不小于三个字符',
            'max_length': '密码长度不大于30个字符'
        })
    captcha = CaptchaField(label='验证码',required=True,error_messages={'required':'验证码不能为空'})






