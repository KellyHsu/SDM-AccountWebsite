from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_date = models.DateField(blank=False)

    def __unicode__(self):
        return unicode(self.user)
