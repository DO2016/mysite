# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-03 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Product created date'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Product last update date'),
        ),
    ]
