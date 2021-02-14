# Generated by Django 3.0.5 on 2021-02-14 09:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_auto_20210214_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockitem',
            name='adj_close',
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='reg_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 14, 9, 41, 24, 920503, tzinfo=utc), null=True),
        ),
    ]
