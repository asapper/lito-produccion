# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-09 00:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('control_produccion', '0008_auto_20160808_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 9, 0, 16, 43, 941458, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
