import hashlib
import logging

from random import randint

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django_redis.serializers import json

from pymysql import DatabaseError

from Mall.settings import SMSCONFIG
from userinfo.forms import UserForm, LoginForm
from userinfo.models import GoodsType, UserInfo, Goods, CartInfo
from userinfo.yzm_login import send_sms

from cart.cart import Cart


# 首页
def index(request):
    if request.method == 'GET':
        new_goods = Goods.objects.order_by('id')[:12]
    return render(request, 'index.html', {'new_goods': new_goods})


# 注册
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
            return redirect(reverse('mall:login'))
    else:
        form = UserForm()
    return render(request, 'register.html', context={'form': form})


# 登陆
def login_(request):
    new_user = LoginForm(request.POST)
    if new_user.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        res = UserInfo.objects.filter(username=username, password=password).values('username', 'id')
        if len(res) > 0:
            request.session['uid'] = res[0]['id']
            request.session['username'] = res[0]['username']
        return redirect(reverse('mall:index'))
    new_user = LoginForm()
    return render(request, 'login.html', context={'new_user': new_user})


# 退出登陆
def logout(request):
    request.session.flush()
    return redirect(reverse('mall:index'))


# 商品列表
def list(request):
    if request.method == 'GET':
        new_goods = Goods.objects.order_by('id')[:5]
        goods = Goods.objects.order_by('price')
    return render(request, 'liebiao.html', context={'new_goods': new_goods, 'goods': goods})


def list1(request):
    if request.method == 'GET':
        new_goods = Goods.objects.order_by('id')[5:10]

    return render(request, 'liebiao.html', context={'new_goods': new_goods})


def list2(request):
    if request.method == 'GET':
        new_goods = Goods.objects.order_by('id')[10:15]

    return render(request, 'liebiao.html', context={'new_goods': new_goods})


def list3(request):
    if request.method == 'GET':
        new_goods = Goods.objects.order_by('id')[15:20]

    return render(request, 'liebiao.html', context={'new_goods': new_goods})


def list4(request):
    if request.method == 'GET':
        new_goods = Goods.objects.order_by('id')[20:25]

    return render(request, 'liebiao.html', context={'new_goods': new_goods})


def list5(request):
    if request.method == 'GET':
        new_goods = Goods.objects.order_by('id')[25:30]

    return render(request, 'liebiao.html', context={'new_goods': new_goods})


# 商品详情页
def detail(request):
    id = request.GET.get('id')
    goods = Goods.objects.filter(pk=id).first()
    return render(request, 'xiangqing.html', {'goods': goods})


# 添加购物车
def add_cart(request):
    # 获取商品id和数量
    new_cart = CartInfo()
    good_id = request.GET.get('good_id')
    good_count = request.GET.get('good_count')
    user_id = request.session.get('user_id')
    c_good = Goods.objects.filter(id=good_id)
    c_user = UserInfo.objects.get(id=user_id)
    # 判断
    if len(c_good) > 0:
        new_cart.user = c_user
        new_cart.good = c_good
    else:
        return HttpResponse('没有该商品，添加失败')
    new_cart.count = int(good_count)
    try:
        oldgo = CartInfo.objects.filter(user_id=user_id, goods_id=good_id)
        if len(oldgo) > 0:
            oldgo[0].ccount = oldgo[0].ccount + new_cart.count
            oldgo[0].save()
        else:
            new_cart.save()
    except DatabaseError as e:
        logging.warning(e)

    return HttpResponse('添加成功')




# 购物车
def cart(request):
    id = request.session.get('id')
    check_foods = CartInfo.objects.filter(user_id=id)
    return render(request, 'gouwuche.html', {'check_goods': check_foods})


def cart_num(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        count = len(session_goods) if session_goods else 0

        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


# 购物车中的总价
def cart_price(request):
    # 存储在session中的goods
    session_goods = request.session.get('goods')
    all_total = len(session_goods) if session_goods else 0
    all_price = 0  # 购物车当前价格
    is_selected_num = 0  # 勾选次数
    for se_goods in session_goods:
        if se_goods[2]:
            goods = Goods.objects.filter(pk=se_goods[0]).first()
            # 购物车价格等于商品售价×商品数量+当前购物车价格
            all_price += goods.price * se_goods[1]
            is_selected_num += 1  # 勾选次数+1

            return JsonResponse({
                'code': 200,
                'msg': '请求成功',
                'all_total': all_total,
                'all_price': all_price,
                'is_selected': is_selected_num,
            })


# 购物车选择状态和数量修改
# { goods_id,num,is_select }
def change_cart(request):
    goods_id = int(request.POST.get('goods_id'))
    goods_num = request.POST.get('goods_num')
    goods_select = request.POST.get('goods_select')

    # 修改
    session_goods = request.session.get('goods')
    for se_goods in session_goods:
        if se_goods[0] == goods_id:
            se_goods[1] = int(goods_num) if goods_num else se_goods[1]
            se_goods[2] = int(goods_select) if goods_select else se_goods[2]

    request.session['goods'] = session_goods

    return JsonResponse({'code': 200, 'mag': '请求成功'})


# 删除购物车
def delete_cart(request):
    # 删除购物车的商品信息 { goods_id,num,is_select}
    goods_id = int(request.POST.get('goods_id'))
    goods_num = request.POSt.get('goods_num')

    session_goods = request.session.get('goods')
    # 下标删除
    if len(session_goods) > 1:
        for index in range(len(session_goods) - 1):
            if session_goods[index][0] == goods_id:
                del session_goods[index]
    else:
        del session_goods[0]
    request.session['goods'] = session_goods
    user_id = request.session.get('user_id')
    if user_id:
        CartInfo.objects.filter(user_id=user_id, goods_id=goods_id).delete()
    return JsonResponse({'code': 200, 'msg': '删除成功'})


# 修改购物车中的勾选状态
def change_status_cart(request):
    goods_id = int(request.POST.get('goods_id'))
    goods_num = request.POST.get('goods_num')
    goods_select = request.POST.get('goods_select')
    select = 0
    if int(goods_select) == 1:
        select = 0
    else:
        select = 1

    session_goods = request.session.get('goods')
    for se_goods in session_goods:
        if se_goods[0] == goods_id:
            se_goods[2] = select

    request.session['goods'] = session_goods

    return JsonResponse({'code': 200, 'msg': '请求成功'})


# 个人中心
def center(request):
    return render(request, 'self_info.html')


def edit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        res = UserInfo.objects.filter(username=username, phone=phone).values('username', 'id')
        if len(res) > 0:
            request.session['uid'] = res[0]['id']
            request.session['username'] = res[0]['username']
            request.session['phone'] = res[1]['phone']
        return redirect(reverse('mall:edit'))
    return render(request, 'self_info.html')


def order_center(request):
    return render(request, 'dingdanzhongxin.html')
