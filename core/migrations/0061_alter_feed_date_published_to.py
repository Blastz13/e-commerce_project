# Generated by Django 3.2.5 on 2021-08-04 07:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_alter_feed_date_published_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 11, 7, 3, 5, 556905, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
