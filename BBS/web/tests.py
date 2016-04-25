# coding:utf-8
from django.test import TestCase

# Create your tests here.

data_list = [
    (None,'A'),
    ('A','A1'),
    ('A','A1-1'),
    ('A1','A2'),
    ('A1-1','A2-3'),
    ('A2-3','A3-4'),
    ('A1','A2-2'),
    ('A2','A3'),
    ('A2-2','A3-3'),
    ('A3','A4'),
    (None,'B'),
    ('B','B1'),
    ('B1','B2'),
    ('B1','B2-2'),
    ('B2','B3'),
    (None,'C'),
    ('C','C1'),

]


def tree_search(data_dict, parent, son):
    for k, v_dic in data_dict.items():   # {'A':{}}  从字典的第一层开始判断 k = 'A'
        if k == parent:
            data_dict[k][son] = {}     # 我们需要把son设置为下一层的数据 {'A':{‘A2’:{} } }
            # print "tree", data_dict
            return
        else:    # 如果不相等，说明就没有找到父亲，那么就去掉一层，往下一层去找
            tree_search(data_dict[k], parent, son)
            # print "find_tree", data_dict


data_dict = {}  # 定义一个空字典用来存放循环的层级数据('A','A1')


for item in data_list:
    parent, son = item    # 遍历字典的每一个元组中的两个值

    # 如果parent为空，说明它就是顶级评论
    if parent is None:
        data_dict[son] = {}   # 将顶son值设置为顶级评论。  {'A':{}}

    else:   # 如果parent不为空，说明它应该是下层数据，需要找到它的父亲，并确定父亲在字典中的位置。
            # 循环找的方法不可取，这里用递归的方法，一层一层的去找
        tree_search(data_dict, parent, son)
                                        # {'A':{‘A2’:{} } }
        # print data_dict


for i, v in data_dict.items():
    print i, v
