# Generated by Django 3.0.4 on 2022-04-26 13:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_auto_20220426_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 3, 13, 58, 57, 937153, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
