# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-04 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding_challenge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='challengeattempt',
            name='pass_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
