# Generated by Django 2.1b1 on 2018-12-28 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20181228_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='content',
            field=models.TextField(help_text='Write Your thought here...', max_length=15000),
        ),
    ]
