# Generated by Django 2.1b1 on 2018-12-22 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_posts_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='user',
        ),
        migrations.AlterField(
            model_name='posts',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.Profile'),
        ),
    ]
