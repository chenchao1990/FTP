#!/usr/bin/env python
# _*_coding:utf-8 _*_

import sys
import os

#BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#os.path.abspath 绝对路径 os.path.dirname(__file__) 当前目录，相对路径


#print BASE_DIR
sys.path.append(BASE_DIR)

from modules import main

if __name__ == '__main__':
    EntryPoint = main.ArgvHandler(sys.argv)









