# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-20 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wet_storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plate',
            name='lastusedwell',
            field=models.CharField(default='A1', max_length=4),
        ),
    ]
