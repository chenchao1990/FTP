#!/usr/bin/env python
# -*- coding:utf-8 -*-

c_dic = {}

l = [(None, 'F'), ('a', 'b'), ('c', 'd')]

for comment_obj in l:
    if comment_obj[0] is None:
        print comment_obj[0]
        c_dic[comment_obj] = {}

print c_dic



















data = [
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

#
# def tree_search(d_dic, parent, son):
#     for k,v_dic in d_dic.items():
#         if k == parent: #find your parent
#             d_dic[k][son] = {}
#             print("find parent of :", son)
#             return
#         else: # might in the deeper layer
#             print("going to furhter layer...")
#             tree_search(d_dic[k],parent,son)
#
#
# data_dic = {}
#
# for item in data:
#     parent,son = item
#     if parent is None:# has no parent
#         data_dic[son] ={}
#     else: #  looking for its parent
#         tree_search(data_dic,parent,son)
#         print data_dic
# for k,v in data_dic.items():
#     print(k,v )

'''
data_dic = {
    'A': {
        'A1': {
            'A2':{
                'A3':{
                    'A4':{}
                }
            },
            'A2-2':{
                'A3-3':{}
            }
        }
    },
    'B':{
        'B1':{
            'B2':{
                'B3':{}
            },
            'B2-2':{}
        }
    },
    'C':{
        'C1':{}
    }

}'''