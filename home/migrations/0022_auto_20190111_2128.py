# Generated by Django 2.1b1 on 2019-01-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20190111_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='trending_ratio',
            field=models.FloatField(default=1),
        ),
    ]
