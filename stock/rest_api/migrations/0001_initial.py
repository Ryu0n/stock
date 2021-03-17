# Generated by Django 3.0.5 on 2021-03-17 13:07

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockMarket',
            fields=[
                ('stock_market_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='StockUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StockItemList',
            fields=[
                ('stock_item_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('stock_market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.StockMarket')),
            ],
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateField(default=datetime.datetime(2021, 3, 17, 13, 7, 28, 626486, tzinfo=utc), null=True)),
                ('high', models.FloatField(default=0.0)),
                ('low', models.FloatField(default=0.0)),
                ('open', models.FloatField(default=0.0)),
                ('close', models.FloatField(default=0.0)),
                ('volume', models.FloatField(default=0.0)),
                ('stock_item_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.StockItemList')),
            ],
        ),
    ]
