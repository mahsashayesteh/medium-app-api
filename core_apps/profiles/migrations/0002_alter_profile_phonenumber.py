# Generated by Django 4.1.7 on 2024-08-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="phonenumber",
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
