# Generated by Django 2.1b1 on 2019-01-03 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_auto_20190103_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='follows',
            new_name='followed_by',
        ),
    ]
