# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20181010_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='comments_counter',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]