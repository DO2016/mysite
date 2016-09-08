# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0004_auto_20160907_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='M2ModelBase1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('col1', models.CharField(max_length=400, verbose_name='first name, last name')),
            ],
        ),
        migrations.CreateModel(
            name='M2ModelBase2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('col2', models.CharField(max_length=400, verbose_name='first name, last name')),
                ('col3', models.ManyToManyField(to='app2.M2ModelBase1')),
            ],
        ),
    ]
