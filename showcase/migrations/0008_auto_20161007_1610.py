# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-07 13:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0007_auto_20161007_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
