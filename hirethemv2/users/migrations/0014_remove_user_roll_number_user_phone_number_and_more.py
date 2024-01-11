# Generated by Django 4.2.6 on 2024-01-09 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_rename_twelfth_percentage_user_twelth_percentage_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="roll_number",
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.PositiveBigIntegerField(
                blank=True, max_length=10, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="urn_number",
            field=models.CharField(blank=True, max_length=16, null=True, unique=True),
        ),
    ]
