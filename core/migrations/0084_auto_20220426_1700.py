# Generated by Django 3.0.4 on 2022-04-26 14:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_auto_20220426_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 3, 14, 0, 32, 825135, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
