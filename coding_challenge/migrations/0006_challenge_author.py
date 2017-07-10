# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 23:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coding_challenge', '0005_auto_20170618_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]