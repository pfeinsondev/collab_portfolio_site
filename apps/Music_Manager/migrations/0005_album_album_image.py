# Generated by Django 3.0.5 on 2020-05-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music_Manager', '0004_auto_20200531_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='album_image',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]