# Generated by Django 2.1b1 on 2018-12-20 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_posts_up_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='up_vote',
        ),
    ]
