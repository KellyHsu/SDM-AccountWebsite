from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_date = models.DateField(blank=False)

    def __unicode__(self):
        return unicode(self.user)
