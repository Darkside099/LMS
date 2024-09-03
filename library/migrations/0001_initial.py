# Generated by Django 5.0.7 on 2024-07-23 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "user_ID",
                    models.CharField(
                        max_length=8, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("user_name", models.CharField(max_length=100)),
                ("user_phone", models.CharField(max_length=10, unique=True)),
                ("user_address", models.CharField(max_length=250)),
                ("user_dob", models.DateField()),
            ],
        ),
    ]
