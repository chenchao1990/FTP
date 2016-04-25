"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web.views import index
from web.views import category
from web.views import article_detail
from web.views import article_new
from web.views import account



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index.index, name='index'),
    url(r'^category/(\d+)/$', category.category, name="category"),
    url(r'^article/(\d+)/$', article_detail.article_detail, name="article_detail"),
    url(r'^article/new/$', article_new.article_new, name="article_new"),
    url(r'^logout/$', account.acc_logout, name="logout"),
    url(r'^login/$', account.acc_login, name="login"),


]
