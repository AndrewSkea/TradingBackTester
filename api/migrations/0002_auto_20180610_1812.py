# Generated by Django 2.0.3 on 2018-06-10 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backtest',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('json_config', models.TextField()),
                ('time_taken', models.FloatField()),
                ('num_bought_won', models.IntegerField()),
                ('num_sold_won', models.IntegerField()),
                ('num_bought_failed', models.IntegerField()),
                ('num_sold_failed', models.IntegerField()),
                ('exp_profit', models.TextField()),
                ('linear_profit', models.IntegerField()),
                ('lowest_balance', models.IntegerField()),
                ('starting_balance', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Bucketlist',
        ),
    ]