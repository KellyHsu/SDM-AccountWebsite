# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 04:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20161205_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classification',
            old_name='classificaion_type',
            new_name='classification_type',
        ),
    ]
