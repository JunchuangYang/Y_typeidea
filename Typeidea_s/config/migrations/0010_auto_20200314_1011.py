# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-14 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_auto_20200312_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(2, '最新文章'), (4, '最近评论'), (3, '最热文章'), (1, 'HTML')], default=1, verbose_name='展示类型'),
        ),
    ]