# Generated by Django 4.1.3 on 2022-11-18 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_alter_company_options_alter_job_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="link",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
    ]
