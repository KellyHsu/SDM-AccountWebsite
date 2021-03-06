# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 04:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
        ('account', '0004_budget_cyclicalexpenditure'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.IntegerField()),
                ('reminder', models.IntegerField()),
                ('is_reminded', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member')),
            ],
        ),
        migrations.AddField(
            model_name='budget',
            name='is_reminded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cyclicalexpenditure',
            name='is_reminded',
            field=models.BooleanField(default=False),
        ),
    ]
