# Generated by Django 3.0.4 on 2022-04-26 13:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Скидка %'),
        ),
    ]
