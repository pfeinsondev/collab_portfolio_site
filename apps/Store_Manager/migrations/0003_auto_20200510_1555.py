# Generated by Django 3.0.5 on 2020-05-10 15:55

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store_Manager', '0002_auto_20200510_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='item_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/media/images/'), upload_to=''),
        ),
    ]