# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0004_load_intial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='token',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
