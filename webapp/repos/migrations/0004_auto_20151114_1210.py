# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repos', '0003_repo_downloaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repo',
            name='branch',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='repo',
            name='revision',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
