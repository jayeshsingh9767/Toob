# Generated by Django 2.1b1 on 2019-01-08 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_posts_types'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='types',
            new_name='type',
        ),
    ]
