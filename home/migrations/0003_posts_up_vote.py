# Generated by Django 2.1b1 on 2018-12-20 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_upvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='up_vote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Upvote'),
        ),
    ]
