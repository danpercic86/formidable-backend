# Generated by Django 3.2a1 on 2021-02-13 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administration", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
