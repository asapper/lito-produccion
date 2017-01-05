# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-09 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_produccion', '0013_auto_20160809_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='id',
        ),
        migrations.AlterField(
            model_name='group',
            name='group_sh_id',
            field=models.PositiveSmallIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order_group',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_produccion.Group'),
        ),
    ]
