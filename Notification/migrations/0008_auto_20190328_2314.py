# Generated by Django 2.1b1 on 2019-03-28 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0007_auto_20190223_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='sender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='signup.Profile'),
        ),
    ]