# Generated by Django 3.0.4 on 2021-07-05 08:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_auto_20210705_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='date_published_to',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 12, 8, 38, 53, 66855, tzinfo=utc), null=True, verbose_name='Опубликовать до'),
        ),
    ]
