# Generated by Django 5.1.3 on 2024-12-18 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bus_id", models.CharField(max_length=100, unique=True)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("route_id", models.CharField(max_length=100)),
                ("vehicle_number", models.CharField(max_length=50)),
            ],
        ),
    ]
