# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('branch', models.CharField(max_length=200)),
                ('revision', models.CharField(max_length=200)),
            ],
        ),
    ]
