# Generated by Django 2.0.3 on 2018-06-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backtest',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]