# Generated by Django 4.0.8 on 2022-11-24 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_profile_picture_alter_user_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='defaults/profiles/default.jpg', null=True, upload_to='photos/profiles'),
        ),
    ]