#!/usr/bin/env python
# _*_coding:utf-8 _*_


import json

acc_dic = {
    'chenchao':{"password":"pwd@123",
                "quotation":10000,
                "expire_date":"2016-1-15",},
    'zhangsan':{"password":"123456",
                "quotation":10000,
                "expire_date":"2016-1-16",},
    'lisi':{},
            }

f = file("accounts.json","wb")
json.dump(acc_dic,f)
f.close()