# Generated by Django 4.0.8 on 2022-11-27 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_alter_job_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-last_date', '-created']},
        ),
    ]
