# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-12 11:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_movie_total_seasons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='comments_counter',
            new_name='total_comments',
        ),
    ]