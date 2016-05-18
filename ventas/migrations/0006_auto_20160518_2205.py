# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-18 22:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_auto_20160118_0810'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_authorized', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authorizedquote',
            name='quote',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ventas.Quote'),
        ),
    ]