# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit3', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Samplestatus',
            fields=[
                ('samplestatusid', models.AutoField(primary_key=True, serialize=False)),
                ('samplestatus', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'samplestatus',
                'managed': False,
            },
        ),
    ]
