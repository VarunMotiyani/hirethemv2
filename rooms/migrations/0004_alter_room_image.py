# Generated by Django 4.0.8 on 2022-11-26 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_room_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, default='defaults/rooms/defaults.webp', null=True, upload_to='room/photos'),
        ),
    ]