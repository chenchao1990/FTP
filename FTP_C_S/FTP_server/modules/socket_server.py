#!/usr/bin/env python
# _*_coding:utf-8 _*_

'''
创建socket的对象
'''
from conf import settings
import SocketServer
import json
import auth
import os
import hashlib
import time
import sys

class FtpServer(SocketServer.BaseRequestHandler):

    respons_code = {
            '200':"User pass authentication!",
            '201':"Invalid username or password",
            '202':"User expried",
            '300':"File ready to send!",
            '301':"File ready to recv!",
        }

    def handle(self):
        shut_down_flag = False
        while not shut_down_flag:
            data = self.request.recv(1024)  #接受客户端发送过来的json格式的数据
            self.data_parser(data)    #交给数据分析的方法处理

    def data_parser(self,data):   #处理客户端发送过来的数据方法
        data = json.loads(data)
        if data.get("action"):  #如果发送过来的数据有内容说明正确
            action_type = data.get("action")    #发送过来action的动作，是认证，还是发送文件等等
            if hasattr(self,action_type):     #如果对象下面有这个方法
                func = getattr(self,action_type)  #反射调用用户验证的方法
                func(data)
            else:                               #如果对象下面没有这个方法
                print "invalid client type!!!"
        else:                                    #客户端发送过来的数据不合格
            print "invalid client data",data

    def cmd__get(self,data):                        #处理发送的命令的方法
        if hasattr(self,"login_user"):                #判断是否存在账户信息，有则验证已经通过，没有则没通过
            filename_path = data.get("filename")   #用户传过来的文件名,可能是带有目录的
            filename_path = filename_path.encode('utf-8')
            file_with_abs_path = "%s%s" % (self.home_path,filename_path)  #拼接  用户家目录+文件名
            if os.path.isfile(file_with_abs_path):               #如果存在这个文件
                file_size = os.path.getsize(file_with_abs_path)   #获取这个文件的大小
                response_data = {"status":"300",
                                 "data":[
                                     {"filename":filename_path,
                                      "size":file_size}]}
                self.request.send(json.dumps(response_data))         #将定义好的字典发送到客户端
                # print  "send to  client dic============================="
                client_response = json.loads(self.request.recv(1024))   #等待接收客户端发来商议好的字典
                # print  "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                if client_response.get("status") == 302:    #断点续传
                    print "\033[33;1mStart file continue send!!!\033[0m"
                    client_file_size = client_response.get("client_file_size")
                    f = open(file_with_abs_path,"rb")
                    begin_size = client_file_size
                    residual_size = file_size - begin_size   #文件还剩下的大小
                    send_size = 0
                    while send_size != residual_size:
                        f.seek(begin_size)
                        data = f.read(4096)
                        self.request.send(data)
                        send_size += len(data)
                    else:
                        f.close()

                elif client_response.get("status") == 301:            #如果status =301 就开始传文件
                    print "start sending file !!~~~~~~"
                    f = open(file_with_abs_path,"rb")
                    send_size = 0
                    file_md5 = hashlib.md5()    #创建md5对象
                    while file_size != send_size:
                        data = f.read(4096)
                        self.request.send(data)         #发送4096个数据
                        send_size += len(data)
                        file_md5.update(data)            #将读取的数据传入加密对象中
                        #print file_size,send_size

                    else:
                        md5_str = file_md5.hexdigest()            #将读取的数据生成一个md5验证码
                        print md5_str
                        self.request.recv(1024)             #防止粘包
                        self.request.send(md5_str)              #将验证码发送到客户端###############
                        print "\033[33;1msend file done\033[0m"
                        f.close()

            else:
                print "file is not find"
        else:
            print "User login faild!!!!"

    def user_auth(self,data):    #用户验证方法，方法名必须是服务端和客户端商议好的名称。
        #用户验证方法 这里的账户信息即可以支持文件有可以支持数据库，两者的存取方式不同
        #在这里可以要处理多种情况，因此不要在这里写如何读取用户名和密码
        username = data.get("username")
        password = data.get("password")
        auth_mag,auth_status = auth.authentication(username,password) #把信息交给认证模块去验证,返回的是结果信息和True或False
        if auth_status is  True:  #如果返回status是True 则成功，否则失败
            #在服务器端认证成功，那么客户端在发送数据时就不需要再次认证了。
            w = settings.USER_BASE_HOME_PATH
            b = username.encode(encoding='utf-8')  #这里很坑爹！！
            self.home_path = "%s%s\\" % (w,b)               #获得用户的家目录，以便传文件
            self.login_user = username                      #设置一个变量，确认客户端已经验证通过，以后无需验证
            print "Auth Successful....................",auth_mag
            response_data = {'status':'200',"data":[]}

        else:
            print "Auth faild...............!!!!!!!!!",auth_mag
            response_data = {'status':'201',"data":[]}
        self.request.send(json.dumps(response_data))   #向客户端发送认证的结果



