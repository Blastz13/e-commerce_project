# Generated by Django 3.0.4 on 2020-04-08 18:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20200408_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 15, 18, 47, 53, 963710, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
