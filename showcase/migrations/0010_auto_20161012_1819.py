# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-12 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0009_auto_20161010_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='products',
            field=models.ManyToManyField(related_name='ings', through='showcase.Composition', to='showcase.Product', verbose_name='Products with this ingredient'),
        ),
    ]
