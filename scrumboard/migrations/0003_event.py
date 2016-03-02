# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrumboard', '0002_item_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('change', models.SmallIntegerField(choices=[(1, 'Estimate Increased'), (-1, 'Estimate Decreased')], default=1)),
                ('value', models.PositiveSmallIntegerField(default=0)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrumboard.Sprint')),
            ],
        ),
    ]
