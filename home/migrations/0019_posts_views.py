# Generated by Django 2.1b1 on 2019-01-11 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20190108_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='views',
            field=models.PositiveIntegerField(default=1),
        ),
    ]