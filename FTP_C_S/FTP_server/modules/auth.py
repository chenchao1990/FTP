#!/usr/bin/env python
# _*_coding:utf-8 _*_
'''
获得用户信息存储的引擎，验证用户是否存在！！！！
'''

from  conf import  settings
import json
import  sys


def fetch_account():   #获取到账户信息引擎，是文件或者数据库。验证用户名。密码

    acc_storage = settings.ACCOUNT_DB.get("engine")  #获取存储用户信息的方式，文件或者数据库


    if hasattr(sys.modules[__name__],"engine_"+acc_storage): #sys.modules[__name__]
        obj = getattr(sys.modules[__name__],"engine_"+acc_storage)  #得到engine+类型的方法或者类
        return obj()   #执行这个类. return obj() 是返回执行obj这个类的返回的结果给了调用者authentication


def authentication(user,passwd):
    engine_obj = fetch_account()
    return engine_obj.auth(user,passwd)


class engine_file():  #如果存储用户信息引擎为文件

    def auth(self,user,passwd):  #每一个账户引擎里面必须有一个方法叫做auth
        filename = settings.ACCOUNT_DB.get("name")
        assert filename is not None  #可以写成try...except... assert在这里意思是如果返回的结果为空，那么程序就崩溃退出
        f = file(filename,'rb')
        acc_dic = json.load(f)  #将用户信息加载到此
        user_in_db = acc_dic.get(user)
        if user_in_db:
            if passwd == user_in_db.get("password"):
                msg = "Auth was passed!!!!"
                status = True
            else:
                msg = "Password is Error!!!!!"
                status = False
        else:

            msg = "No this User info!!!!"
            status = False
        return msg,status


class engine_mysql():       #如果存储用户信息引擎为Mysql

    def auth(self,user,passwd):#每一个账户引擎里面必须有一个方法叫做auth
        print  "This is engin_mysql_func"