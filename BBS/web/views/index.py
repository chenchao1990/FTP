# coding:utf-8
from django.shortcuts import render
from web import models
from fenye import Pager

# Create your views here.


def index(request):

    current_page = request.GET.get('page', 1)    # 获取前端页面点击的当前页
    page_obj = Pager(current_page)
    # 从数据库中获取设计的每页显示数据的条数
    data_obj = models.Article.objects.all()[page_obj.start: page_obj.end]   # 页面显示分页的个数
    data_all_obj = models.Article.objects.all().count()   # 获取数据库中所有数据的总条数
    print "----------> all date", data_all_obj,type(data_all_obj)

    pager_str = page_obj.page_str(data_all_obj, "?page=")     # 根据总的条数来拼接前端需要的标签字符串
    return render(request, 'index.html', {'articles': data_obj, 'page_str': pager_str})
