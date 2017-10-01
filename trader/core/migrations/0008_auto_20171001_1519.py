# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 18:19
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations
import trader.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20171001_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btcorder',
            name='amount_brl',
            field=trader.core.models.CryptAmount(decimal_places=6, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='BRL amount'),
        ),
        migrations.AlterField(
            model_name='btcorder',
            name='amount_btc',
            field=trader.core.models.CryptAmount(decimal_places=6, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='BTC amount'),
        ),
        migrations.AlterField(
            model_name='fundstransfer',
            name='amount_brl',
            field=trader.core.models.CryptAmount(decimal_places=6, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='BRL amount'),
        ),
    ]
