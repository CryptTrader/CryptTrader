# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20171001_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btcorder',
            name='type',
            field=models.CharField(choices=[('BUYBTC', 'BTC Buy Order'), ('SELLBTC', 'BTC Sell Order')], default='PENDING', max_length=255, verbose_name='type'),
        ),
    ]
