# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-17 00:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0003_auto_20160117_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executive',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='personal.Person'),
        ),
    ]
