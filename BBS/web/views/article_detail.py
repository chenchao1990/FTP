# coding:utf-8
from django.shortcuts import render
from web import models
from django.core.exceptions import ObjectDoesNotExist


def article_detail(request, article_id):

    try:
        article_obj = models.Article.objects.get(id=article_id)

    except ObjectDoesNotExist as e:
        return render(request, '404.html', {'err_msg': u"文章不存在!!!"})

    return render(request, 'article.html', {'article_obj': article_obj})
