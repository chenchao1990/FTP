from __future__ import unicode_literals

from django.db import models
from web.models import UserProfile


class QQGroups(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, default="Nothing")
    members = models.ManyToManyField(UserProfile, blank=True)
    admins = models.ManyToManyField(UserProfile, related_name="group_admins")
    max_menbers_nums = models.IntegerField(default=200)

    def __unicode__(self):
        return self.name