# Generated by Django 3.0.7 on 2020-06-06 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour_Manager', '0003_auto_20200419_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='tour_image',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]