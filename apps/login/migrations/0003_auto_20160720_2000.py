# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20160720_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(default="Welcome to the Group! You can edit your personal description by clicking on the 'Edit Profile' button", max_length=1000),
        ),
    ]
