# Generated by Django 3.0.4 on 2020-08-12 22:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20200813_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 19, 22, 48, 3, 453691, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
