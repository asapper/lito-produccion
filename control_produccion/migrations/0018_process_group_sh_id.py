# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-10 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_produccion', '0017_auto_20160810_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='group_sh_id',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]