import hashlib
import logging

import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

# 首页
from django.urls import reverse

from pymysql import DatabaseError

from userinfo.forms import UserForm
from userinfo.models import GoodsType, UserInfo


def index(request):
    # 展示商品功能
    # 查询分类
    # 该类下全部商品
    a = []
    types = GoodsType.objects.all()
    for type in types:
        b = {}
        b['type'] = type.title
        good_type = get_object_or_404(GoodsType,title = type.title)
        f_goods = random.sample(list(good_type.goods_set.all()),2)
        b['goods'] = f_goods
        a.append(b)
    return render(request,'index.html',context={'good_list':locals()})



def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # 删除repassword
            del form.cleaned_data['repassword']
            print(form.cleaned_data['username'])
            print(form.cleaned_data)
            # 写入数据库
            UserInfo.objects.create(**form.cleaned_data)
            return redirect(reverse('mall:index'))
    else:
        form = UserForm()
    return render(request,'register.html',context={'form':form})

# 登陆
def login_(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        res = UserInfo.objects.filter(username=username,password=password).values('username','id')
        if len(res) > 0:
            request.session['uid'] = res[0]['id']
            request.session['username'] = res[0]['username']
            return redirect(reverse('mall:index'))
    return render(request,'login.html',{'msg':'用户名不存在'})

    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     # 验证用户名和密码是否正确，正确返回user对象
    #     user = authenticate(request,username=username,password=password)
    #     if user:
    #         login(request,user)
    #         return redirect(reverse('mall:index'))
    #         # 未激活
    #     else:
    #         user = UserForm.objectes.filter(username=username)
    #         if user and user[0].is_activate
    #             return HttpResponse('用户未激活')

    