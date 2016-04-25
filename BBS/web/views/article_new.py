# coding:utf-8
from django.shortcuts import render
from web import models
from web.forms import article_new as ArticleForm
from web.forms import upload_file


def article_new(request):

    if request.method == "POST":
        article_form = ArticleForm.ArticlNew(request.POST, request.FILES)
        if article_form.is_valid():
            # print ("--form data:",article_form.cleaned_data)
            form_data = article_form.cleaned_data
            form_data['author_id'] = request.user.userprofile.id  # 反向查找将作者传入到form字典中

            new_img_path= upload_file.handle_upload_file(request, request.FILES['head_img'])
            print new_img_path
            form_data['head_img'] = new_img_path   # 将新的图片路径保存到form字典中
            article_new_obj = models.Article(**form_data)     # 不用object.create方法创建。
            article_new_obj.save()
            return render(request, 'article_new.html', {'article_new_obj': article_new_obj})
        # else:
        #     print ('err:',article_form.errors)
    article_list = models.Category.objects.all()
    return render(request, 'article_new.html', {'article_list': article_list})
