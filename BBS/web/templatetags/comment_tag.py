# coding:utf-8
from django import template

register = template.Library()


def tree_search(c_dict, comment_obj):
    for k, v_dic in c_dict.items():
        if k == comment_obj.parent_comment:
            c_dict[k][comment_obj] = {}
            return
        else:
            tree_search(c_dict[k], comment_obj)


def generate_comment_html(sub_comment_dic,margin_left_val):
    html = ""
    for k, v_dic in sub_comment_dic.items():
        html += "<div style='margin-left:%spx' class='comment-node'>" % margin_left_val + k.comment + "</div>"
        if v_dic:
            html += generate_comment_html(v_dic,margin_left_val+15)
    return html


@register.simple_tag
def comment_tree(comment_list):

    comment_dict = {}
    for comment_obj in comment_list:
        if comment_obj.parent_comment is None:
            comment_dict[comment_obj] = {}

        else:
            tree_search(comment_dict, comment_obj)

    html = "<div class='comment-box'>"
    margin_left = 0
    for k, v in comment_dict.items():

        html += "<div class='comment-node'>" + k.comment + "</div>"
        html += generate_comment_html(v, margin_left+15)

    html += "</div>"

    return html
