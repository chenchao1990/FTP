#!/usr/bin/env python
# _*_coding:utf-8 _*_
'''
放置程序的主要的逻辑处理过程代码
'''
import sys
import socket_server

from conf import  settings


class ArgvHandler(object):   #字符串处理

    def __init__(self,args):
        self.args = args   #客户端传入的字符串sys.argv
        print self.args
        self.argv_parser()  #分析传过来的参数

    def argv_parser(self):
        if len(self.args) == 1: #如果参数没有加任何参数 sys.argv最少为1个参数，文件本身
            self.help_msg()

        else:
            if hasattr(self,self.args[1]): #检测对象里面是否有输入的方法，self代表对象本身
                func = getattr(self,self.args[1])  #执行相应的方法
                func()
            else:
                self.help_msg()

    def start(self):
        server = socket_server.SocketServer.ThreadingTCPServer((settings.BIND_HOST,settings.BIND_PORT),socket_server.FtpServer)
        server.serve_forever()

    def stop(self):
        pass

    def help_msg(self):
        msg = '''
        start           :start ftp server
        stop            :stop ftp server
        create_account  :create ftp user account
        help            :print help msg
                '''
        sys.exit(msg)   #程序退出并返回一个帮助信息
