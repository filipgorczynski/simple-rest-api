# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-10 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20181010_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='director',
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ManyToManyField(related_name='movies', to='movie.Director'),
        ),
    ]
