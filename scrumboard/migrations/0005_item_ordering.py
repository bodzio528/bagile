# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-11 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumboard', '0004_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['manual_order']},
        ),
        migrations.AddField(
            model_name='item',
            name='manual_order',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
