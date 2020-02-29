# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-29 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(2, '最新文章'), (3, '最热文章'), (1, 'HTML'), (4, '最近评论')], default=1, verbose_name='展示类型'),
        ),
    ]
