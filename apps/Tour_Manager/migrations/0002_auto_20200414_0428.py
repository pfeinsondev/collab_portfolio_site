# Generated by Django 3.0.5 on 2020-04-14 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour_Manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='show_time',
            field=models.CharField(max_length=25),
        ),
    ]
