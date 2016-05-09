#!/usr/bin/env python
# _*_coding:utf-8 _*_
import  sys,os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#os.path.abspath 绝对路径 os.path.dirname(__file__) 当前目录，相对路径
sys.path.append(BASE_DIR)

from core import socket_client

if __name__ == '__main__':
    EntryPoint = socket_client.FTPClient(sys.argv)