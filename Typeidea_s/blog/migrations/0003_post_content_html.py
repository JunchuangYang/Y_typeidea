# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-11 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200303_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_html',
            field=models.TextField(blank=True, editable=False, verbose_name='正文HTML代码'),
        ),
    ]