# Generated by Django 4.1.5 on 2023-01-24 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrackerApp', '0009_userlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlocation',
            name='totalDistance',
            field=models.FloatField(default=0, verbose_name='totalDistance'),
        ),
    ]