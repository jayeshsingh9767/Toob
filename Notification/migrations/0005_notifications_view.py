# Generated by Django 2.1b1 on 2019-02-09 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0004_auto_20190208_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='view',
            field=models.BooleanField(default=False),
        ),
    ]
