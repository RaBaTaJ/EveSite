# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PubDate', models.DateTimeField(verbose_name='Date & Time')),
                ('TextContent', models.CharField(max_length=1000, verbose_name='Content')),
                ('Author', models.CharField(max_length=50, verbose_name='Author')),
            ],
        ),
    ]
