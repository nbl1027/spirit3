# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-07 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit3', '0004_plateqcresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statements',
            fields=[
                ('statementsid', models.AutoField(primary_key=True, serialize=False)),
                ('statement', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'statements',
                'managed': False,
            },
        ),
    ]