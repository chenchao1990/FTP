# coding:utf-8
from django.shortcuts import render
from web import models
# Create your views here.


def category(request, category_id):

    articles = models.Article.objects.filter(categroy_id=category_id)

    return render(request, 'index.html', {'articles': articles})
