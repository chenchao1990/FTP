# coding:utf-8

from django import forms


class ArticlNew(forms.Form):

    title = forms.CharField(max_length=30, min_length=5)
    summary = forms.CharField(max_length=30, min_length=5)
    head_img = forms.ImageField()
    categroy_id = forms.IntegerField()
    content = forms.CharField(min_length=15)

