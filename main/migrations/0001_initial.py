# Generated by Django 5.1.1 on 2024-09-28 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=15)),
                ("contact_number", models.CharField(max_length=10)),
                ("city", models.CharField(max_length=15)),
                ("age", models.CharField(max_length=2)),
            ],
        ),
    ]
