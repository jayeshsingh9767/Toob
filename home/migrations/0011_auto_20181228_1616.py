# Generated by Django 2.1b1 on 2018-12-28 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_posts_dis_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='dis_like',
            new_name='dis_likes',
        ),
    ]