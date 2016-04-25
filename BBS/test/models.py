# _*_coding:utf-8_*_
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    '''
    帖子表
    '''
    title = models.CharField(u"文章标题",max_length=255,unique=True)
    categroy = models.ForeignKey("Category",verbose_name=u"板块")
    head_img = models.ImageField(upload_to="uploads")
    summary = models.CharField(max_length=255)
    content = models.TextField(u"内容")
    author = models.ForeignKey("UserProfile")
    publish_date = models.DateTimeField(auto_now=True)
    hidden = models.BooleanField(default=True)
    priority = models.IntegerField(u"优先级",default=1000)

    def __unicode__(self):
        return "<%s, author:%s>" %(self.title,self.author)

class Comment(models.Model):
    '''
    存储所有的评论
    '''
    article = models.ForeignKey(Article)
    user = models.ForeignKey("UserProfile")
    #parent_comment = models.ForeignKey('Comment',)
    parent_comment = models.ForeignKey('self',related_name='p_comment',blank=True,null=True)
    comment = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "<%s, user:%s>" %(self.comment,self.user)

class ThumbUp(models.Model):
    '''点赞'''
    article = models.ForeignKey('Article')
    user = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "<user:%s>" %(self.user)

class Category(models.Model):
    '''
    帖子版块
    '''
    name = models.CharField(max_length=64,unique=True)
    admin = models.ManyToManyField('UserProfile')
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    '''
    账户信息表
    '''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    groups = models.ManyToManyField('UserGroup')
    def __unicode__(self):
        return self.name



class UserGroup(models.Model):
    '''
    用户组
    '''
    name = models.CharField(max_length=64,unique=True)

    def __unicode__(self):
        return self.name
