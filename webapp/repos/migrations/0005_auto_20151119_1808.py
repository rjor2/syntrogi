# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repos', '0004_auto_20151114_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='repo',
            name='deletions',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='repo',
            name='files',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='repo',
            name='insertions',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='repo',
            name='lines',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
