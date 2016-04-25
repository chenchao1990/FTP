from django.contrib import admin

# Register your models here.

import models


class CategroyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'hidden', 'publish_date')


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategroyAdmin)
admin.site.register(models.Comment)
admin.site.register(models.ThumUp)
admin.site.register(models.UserProfile)
admin.site.register(models.UserGroup)
