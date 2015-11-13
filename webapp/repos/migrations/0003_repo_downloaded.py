# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repos', '0002_auto_20151113_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='repo',
            name='downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
