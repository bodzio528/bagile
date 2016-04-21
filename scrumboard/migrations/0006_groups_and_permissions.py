# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal
from django.conf import settings

def create_group(apps, schema_editor):
    # Workaround for a Django bug: https://code.djangoproject.com/ticket/23422
    emit_post_migrate_signal(verbosity=0, interactive=False, db='default')

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    for group_name, permission_codenames in settings.GROUPS_PERMISSIONS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        group.permissions.add(*[Permission.objects.get(codename=c) for c in permission_codenames])


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0001_initial'),
        ('scrumboard', '0005_item_ordering'),
    ]

    operations = [
        migrations.RunPython(create_group),
    ]
