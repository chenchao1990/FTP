# coding:utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from web import models


def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def acc_login(request):

    error_meg = ''
    if request.method == "POST":
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        user_obj = authenticate(username=user, password=pwd)  # django自带的验证机制
        # 成功则返回用户对象，失败返回None。这里仅仅是验证成功，并不是登录成功
        if user_obj is not None:
            login(request, user_obj)   # 这里是登录成功，生成session等信息。因为有的时候不需要session
            request.session['IS_login'] = True
            return HttpResponseRedirect('/')

        else:
            error_meg = "用户名或密码错误"

    return render(request, 'login.html', {'error_msg': error_meg})
