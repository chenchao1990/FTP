# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-05 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20160402_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='qq_friends',
            field=models.ManyToManyField(blank=True, null=True, related_name='_userprofile_qq_friends_+', to='web.UserProfile'),
        ),
    ]