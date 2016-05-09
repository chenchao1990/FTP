#!/usr/bin/env python
# _*_coding:utf-8 _*_

import  os
import sys
import  socket
import json
import hashlib

class FTPClient(object):

    respons_code = {
            '200':"User pass authentication!",
            '201':"Invalid username or password",
            '202':"User expried",
            '300':"File ready to send!",
            '301':"File ready to recv!",
            '302':"File is continue recv!"}

    def __init__(self,argv):
        self.args = argv   #用户输入的字符串
        print self.args
        self.parse_argv()  #分析传入的字符串
        self.connect_server()       #连接服务器
        self.handle()       #进行验证和数据交互

    def handle(self):
        if  self.auth():        #如果验证通过了
            self.interactive()    # 交互

    def interactive(self):   # 与服务器交互的方法
        quit_flag = False
        while not quit_flag:  #循环让用户输入指令
            user_input = raw_input("\033[33;1m%s\033[0m][%s]:" % (self.username,self.cwd)).strip()
            if len(user_input) == 0:continue
            self.cmd_parser(user_input)              #将用户数输入的交给命令处理的方法

    def cmd_parser(self,user_input):  #处理用户输入的指令
        cmd_list = user_input.split()  #将用户输入的指令按空格分割为列表
        if hasattr(self,"cmd__"+cmd_list[0]):   #判断是否有此方法
            func = getattr(self,"cmd__"+cmd_list[0])   #获得方法
            func(cmd_list)                  #执行方法，并传入输入的指令
        else:

            print "\033[31;1mInvalid cmd !!!!\033[0m"

    def cmd__get(self,cmd_list):
        if len(cmd_list) <2:
            print "\033[33;1mPlease input file name !!\033[0m"

        else:
            remote_filename = cmd_list[1]  #获取用户输入的文件名
            dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #文件所在的路径
            new_filename = dir_name + "\\" + remote_filename
            have_file = os.path.isfile(new_filename)  #判断目录下是否有此文件


            msg_str = {"action":"cmd__get",   #会写很多这样的字典，可以把它写成一个接口，维护方便。
                       "filename":remote_filename,}
            self.sock.send(json.dumps(msg_str))  #将客户端的下载请求发送到server
            server_response = json.loads(self.sock.recv(1024))  #接受服务端发来的数据-
            #{"status":300,"data":[{"filename":"qqq","size":1234}]}总计
            total_file_size = int(server_response["data"][0].get("size"))  #文件的总大小
            print "\033[31;1mTotal file size is %s\033[0m" % total_file_size


            if have_file == True:            #如果文件已经存在，断点续传
                file_size = os.path.getsize(new_filename)  #当前文件的大小
                print "\033[31;1mLocal file size is %s\033[0m" % file_size
                client_response = {"action":"cmd__get",   #会写很多这样的字典，可以把它写成一个接口，维护方便。
                       "filename":remote_filename,
                       "client_file_size":file_size,
                       "status":302,
                       }                        #print "\033[31;1m \033[0m"
                self.sock.send(json.dumps(client_response))
                print "\033[31;1mSend 302 dict is OK!!!!\033[0m"
                f = open(remote_filename,"ab")
                while file_size != total_file_size:
                    data = self.sock.recv(4096)    #别超过10000
                    file_size += len(data)     #注意接收数据的最后一段大小
                    f.write(data)
                else:
                    print "\033[31;1mThis file  has append over!!!!!\033[0m"
                    f.close()




            else:
                client_response = {"action":"cmd__get",   #会写很多这样的字典，可以把它写成一个接口，维护方便。
                           "filename":remote_filename,
                           "status":301,}
                self.sock.send(json.dumps(client_response))  #发送准备接收的状态 防止粘包
                received_size = 0      #开始接收
                local_filename = os.path.basename(remote_filename)
                f = open(local_filename,"wb")
                file_md5 = hashlib.md5()         #创建md5对象


                while total_file_size != received_size:  #如果不相等，那就一直接收
                    data = self.sock.recv(4096)    #别超过10000
                    received_size += len(data)     #注意接收数据的最后一段大小
                    f.write(data)
                    file_md5.update(data)       #添加加密的数据

                    progress_num = received_size*100 / total_file_size
                    sys.stdout.write("\r[%s%%]" % progress_num+ ">"*progress_num)  #进度条
                    sys.stdout.flush()

                else:
                    f.close()
                    self.sock.send('nothing')       #防止粘包
                    recv_md5 = self.sock.recv(1024)    #接收服务器端发过来的MD5效验码
                    md5_str = file_md5.hexdigest()      #根据接收的最终数据，生成客户端的MD5效验码
                    if recv_md5 ==md5_str:

                        print "\033[31;1m\nfile  download sunccess!!!\033[0m"
                        print "\033[31;1m MD5 Verify success!\033[0m"
                    else:
                        print "\033[31;1m MD5 Verify faild!!!!!\033[0m"



    def auth(self):   #用户交互的方法
        retry_count = 0             #用户输入的次数
        while retry_count <3:
            username = raw_input("username:")
            if len(username) == 0:continue
            password = raw_input("password:")
            if len(password) == 0:continue
            data = json.dumps({"username":username,
                            "password":password,
                            "action":"user_auth",
                            })
            cmd_str = data
            self.sock.send(cmd_str)   #发送用户输入的用户名和密码
            server_response = json.loads(self.sock.recv(1024))  #接受服务器返回的数据 loads回来
            #服务端和客户端都要定义一个相同的字典,在交互时统一数据
            #{"status":"200",data:[]}
            if  server_response["status"] == "200":   #如果返回的“status” =200 验证成功，打印！
                print self.respons_code["200"]  #服务器返回的字典中，要有200的key和对应value
                self.username = username
                self.cwd = "/"
                return True
            else:
                print self.respons_code[server_response["status"]]
                retry_count +=1
        else:
            sys.exit("\033[31;1m Too many try input!!!\033[0m")

    def parse_argv(self):  #处理用户输入的字符串

        if len(self.args) <5:  #如果传入的参数小于5个
            self.help_msg()
        else:
            mandatory_fields = ["-s","-p"]
            for i in mandatory_fields:  #mandatory_fields ：强制字符
                if i not in self.args:  #如果传入的参数里没有 -s 和 -p 则无效
                    sys.exit("The argument [%s] is mandatory!" %i)
            try:
                self.ftp_host = self.args[self.args.index("-s")+1]  #"-s"后面跟的是HOST_IP 所以要+1
                self.ftp_port = int(self.args[self.args.index("-p")+1])  #"-p" 后面跟的是PORT
            except (IndexError,ValueError) as e:  #错误名可以写在一起
                print "\033[31;1m%s\033[0m" % e #打印错误和帮助信息
                self.help_msg()
            #print ftp_host,ftp_port

    def connect_server(self):   #创建socket对象，并连接服务器

        try:
            self.sock = socket.socket()
            self.sock.connect((self.ftp_host,self.ftp_port))
            self.sock.settimeout(5)
        except socket.error as e:
            sys.exit(e)

    def help_msg(self):
        help_msg = '''
        -s ftp_server_addr      :the ftp server you want to connect,mandatory
        -p ftp port             :ftp port ,mandatory
        '''

        sys.exit(help_msg)

