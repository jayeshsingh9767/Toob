# Generated by Django 2.1b1 on 2019-01-11 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20190111_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='trending_ratio',
            field=models.DecimalField(decimal_places=4, default=1, max_digits=8),
        ),
        migrations.AlterField(
            model_name='posts',
            name='type',
            field=models.CharField(choices=[('1', 'Question'), ('2', 'Creative Idea'), ('3', 'Innovation'), ('4', 'Nightmare'), ('5', 'Thought')], max_length=50),
        ),
    ]
