#!/usr/bin/env python
# _*_coding:utf-8 _*_

'''
放置程序的配置参数
'''
import os
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BIND_HOST = '0.0.0.0'
BIND_PORT = 9999

ACCOUNT_DB = {
    'engine': 'file', # mysql,oracle
    #accounts.json是存放用户信息的文件
    'name' : '%s/conf/accounts.json' % BASE_DIR,  #要写绝对路径

}

USER_BASE_HOME_PATH = "%s\\var\\users\\" % BASE_DIR

print USER_BASE_HOME_PATH