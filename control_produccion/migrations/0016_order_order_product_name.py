# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-10 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_produccion', '0015_auto_20160809_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_product_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
