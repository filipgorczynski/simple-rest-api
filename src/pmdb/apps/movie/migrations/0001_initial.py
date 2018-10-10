# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-09 10:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField(blank=True)),
                ('rated', models.CharField(blank=True, max_length=32)),
                ('released', models.DateField(blank=True)),
                ('runtime', models.CharField(blank=True, max_length=16)),
                ('writer', models.TextField(blank=True)),
                ('plot', models.TextField(blank=True)),
                ('language', models.CharField(blank=True, max_length=64)),
                ('country', models.CharField(blank=True, max_length=64)),
                ('awards', models.CharField(blank=True, max_length=255)),
                ('poster', models.URLField(blank=True, max_length=255)),
                ('metascore', models.CharField(blank=True, max_length=16)),
                ('imdb_rating', models.CharField(blank=True, max_length=32)),
                ('imdb_votes', models.CharField(blank=True, max_length=32)),
                ('imdb_id', models.CharField(blank=True, max_length=32)),
                ('type', models.CharField(blank=True, max_length=64)),
                ('dvd', models.DateField(blank=True)),
                ('box_office', models.CharField(blank=True, max_length=255)),
                ('production', models.CharField(blank=True, max_length=255)),
                ('website', models.URLField(blank=True, max_length=255)),
                ('actors', models.ManyToManyField(to='movie.Actor')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Director')),
                ('genre', models.ManyToManyField(to='movie.Genre')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('source', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='ratings',
            field=models.ManyToManyField(to='movie.Rating'),
        ),
    ]