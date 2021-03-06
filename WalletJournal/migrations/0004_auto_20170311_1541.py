# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WalletJournal', '0003_auto_20170310_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='RefID',
            field=models.CharField(default=1, max_length=25, verbose_name='RefID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='BalanceAfterTransaction',
            field=models.FloatField(max_length=75, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='TransactionAmount',
            field=models.FloatField(max_length=75, verbose_name='Amount'),
        ),
    ]
